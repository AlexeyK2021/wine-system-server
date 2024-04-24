class Actuator:
    def __init__(self, id, name, model, ip, port, state_node_id, cmnd_node_id):
        self.id = id
        self.name = name
        self.model = model
        self.ip = ip
        self.port = port
        self.state_node_id = state_node_id
        self.cmnd_node_id = cmnd_node_id

    def __str__(self):
        return f"Id={self.id}; name={self.name}; model={self.model}; ip={self.ip}; port={self.port}; state_node_id={self.state_node_id}; cmnd_node_id={self.cmnd_node_id}"
