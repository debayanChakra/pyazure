from flask import Flask
from flask import jsonify,request,render_template
import azure_networking
import azure_networking_base
import azure_storage
import azure_storage_base
import azure_resource_group_base
import azure_computation_base
import logging
logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def usage_service():
    return render_template('index.html')


@app.route('/ping', methods=['GET','POST'])
def self_service():
    return jsonify(result='pong')


@app.route('/create_vnet/<subscription_id>', methods=['POST'])
def create_vnet(subscription_id):
    resource_group_name = request.args.get('resource_group_name', '')
    vnet_name = request.args.get('vnet_name', '')
    location = request.args.get('location', '')
    address_space = request.args.get('address_space', '')
    obj_virtual_network = azure_networking.BuildNetwork(subscription_id, vnet_name)
    network = obj_virtual_network.build_virtual_network(resource_group_name=resource_group_name, location=location,address_prefix=address_space)
    return jsonify(result=network)


@app.route('/create_subnet/<subscription_id>',methods=['POST'])
def create_subnet(subscription_id):
    vnet_name = request.args.get('vnet_name', '')
    subnet_name = request.args.get('subnet_name', '')
    address_cidr = request.args.get('address_cidr', '')
    location = request.args.get('location', '')
    obj_virtual_network = azure_networking.BuildNetwork(subscription_id, vnet_name)
    network = obj_virtual_network.build_subnet(subnet_name=subnet_name, cidr=address_cidr, location=location)
    return jsonify(result=network)


@app.route('/create_network_peering/<subscription_id>', methods=['POST'])
def create_vnet_peering(subscription_id):
    vnet_name = request.args.get('vnet_name', '')
    remote_vnet_name = request.args.get('remote_vnet_name', '')
    obj_virtual_network = azure_networking.BuildNetwork(subscription_id, vnet_name)
    peering_object = obj_virtual_network.connect_vnet(remote_vnet=remote_vnet_name)
    return jsonify(result=peering_object)


@app.route('/vnet_details/<subscription_id>',methods=['GET'])
def get_network_details(subscription_id):
    vnet_name = request.args.get('vnet_name', '')
    obj_virtual_network = azure_networking.BuildNetwork(subscription_id, vnet_name)
    virtual_network = obj_virtual_network.get_vnet_details(obj_virtual_network.vnet_name)
    return jsonify(result=virtual_network)


@app.route('/list_rgs/<subscription_id>',methods=['GET'])
def get_rg_list(subscription_id):
    obj_rgs = azure_resource_group_base.BaseRg(subscription_id)
    rg_details = obj_rgs.list_rg()
    return jsonify(result=rg_details)


@app.route('/list_vnet/<subscription_id>',methods=['GET'])
def list_all_virtual_network(subscription_id):
    obj_network = azure_networking_base.BaseAzure(subscription_id)
    virtual_network_details = obj_network.list_all_vnet()
    return jsonify(result=virtual_network_details)


@app.route('/list_peering/<subscription_id>',methods=['GET'])
def list_all_peered_vnet(subscription_id):
    vnet_name = request.args.get('vnet_name', '')
    obj_network = azure_networking_base.BaseAzure(subscription_id)
    peering_object=obj_network.get_peering_networks(vnet_name=vnet_name)
    return jsonify(result=peering_object)


@app.route('/get_read_sas/<subscription_id>',methods=['POST'])
def find_sas_with_read_permission(subscription_id):
    storage_name = request.args.get('storage_name', '')
    obj_storage = azure_storage.BuildStorage(subscription_id,storage_name)
    storage_object = obj_storage.fetching_sas()
    app.logger.info('Processing default request')
    return jsonify(result="?"+storage_object['rs'])


@app.route('/get_admin_sas/<subscription_id>',methods=['POST'])
def find_sas_with_write_permision(subscription_id):
    storage_name = request.args.get('storage_name', '')
    obj_storage = azure_storage.BuildStorage(subscription_id,storage_name)
    storage_object = obj_storage.fetching_sas()
    app.logger.info('Processing default request')
    return jsonify(result="?"+storage_object['ws'])




if __name__ == '__main__':
   app.run(host='0.0.0.0')

