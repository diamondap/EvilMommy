import EvilMommy.Config, json
from flask import Flask, request, render_template, redirect, url_for
from EvilMommy.WirelessAccessManager import WirelessAccessManager
from EvilMommy.Security import Security

app = Flask(__name__)
json = json.JSONEncoder()


@app.route('/')
def index():
    return render_template("login.html")



@app.route('/login', methods=['POST'])
def login():
    user = request.form['user']

    # Log to STDOUT during dev
    print ("\nLogin attempty from user  %s\n" % (user))

    if user in EvilMommy.Config.valid_users:
        sec = Security(EvilMommy.Config.encryption_key)
        resp = redirect(url_for('status') + '?msg=Welcome!')
        resp.set_cookie('auth_token', 
                        sec.create_auth_token(user, request.remote_addr))
        return resp
    else:
        return render_template("login.html", message = "Login Incorrect")


@app.route('/logoff')
def logoff():
    resp = redirect(url_for('index'))
    resp.set_cookie('auth_token', '')
    return resp


@app.route('/command_menu')
def command_menu():
    """
    This displays a menu of available commands.
    """
    if not is_valid_user(request):
        return redirect(url_for('index'))
    machines_json = json.encode(EvilMommy.Config.machines)
    return render_template('command_menu.html', machines = machines_json)




@app.route('/run_command', methods=['POST'])
def run_command():
    """
    Executes a command from the user: disable or enable access for
    some device.
    """
    if not is_valid_user(request):
        return redirect(url_for('index'))
    command = request.form['command']
    device = request.form['device']

    # Log to STDOUT during dev
    print ("\nCommand = %s\nDevice = %s\n" % (command, device))

    mgr = WirelessAccessManager(EvilMommy.Config)    
    clients_table = mgr.get_dhcp_clients_table()
    target_device = find_device_by_hostname(device, clients_table)
    if target_device is None:
        target_device = find_device_by_hostname(device, 
                                                EvilMommy.Config.machines)

    if target_device is None:
        err_message = "Request failed. Could not find device entry " + \
                      "in config or in list of router clients."
        return redirect(url_for('status') + '?msg=' + err_message)
    
    removed = False
    blacklited = False
    result_msg = "Request failed."
    if (command == 'disconnect'):
        if ('ip_address' in target_device):
            removed = mgr.remove_from_dhcp_clients_table(target_device['ip_address'])
        else:
            removed = True # Device is not currently connected
        blacklisted = mgr.add_to_blacklist(target_device['mac_address'])
        if (removed and blacklisted):
            result_msg = "Request succeeded."
    elif (command == 'reconnect' and
             mgr.remove_from_blacklist(target_device['mac_address'])):
            result_msg = "Request succeeded."

    return redirect(url_for('status') + '?msg=' + result_msg)




@app.route('/status', methods=['GET'])
def status():
    """
    Display the client list and the MAC blacklist, along with an optional
    message.
    """
    if not is_valid_user(request):
        return redirect(url_for('index'))
    mgr = WirelessAccessManager(EvilMommy.Config)
    msg = request.args['msg']
    return render_template('status.html', 
                           message = msg,
                           clients = mgr.get_dhcp_clients_table(),
                           mac_filters = mgr.get_blacklist())
    
def is_valid_user(request):
    """
    Returns true if user is logged in, false if not.
    """
    sec = Security(EvilMommy.Config.encryption_key)
    token = request.cookies.get('auth_token');
    print token
    return sec.is_valid_user(token, 
                             EvilMommy.Config.valid_users, 
                             request.remote_addr)


def find_device_by_hostname(hostname, entries):
    """
    Finds the entry for the machine with the specifed hostname.
    entries can be either EvilMommy.Config.machines or 
    the list returned from WirelessAccessManager.get_dhcp_clients_table
    """
    for machine in entries:
        if machine['hostname'] == hostname:
            return machine
    return None



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port = 3000)
