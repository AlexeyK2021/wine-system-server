class Sensor:

    def __init__(self, id, name, model, paramId, ip, port, nodeId):
        self.id = id
        self.name = name
        self.model = model
        self.param_id = paramId
        self.ip = ip
        self.port = port
        self.node_id = nodeId

    def __str__(self):
        return f"Id={self.id}; name={self.name}; model={self.model}; paramId={self.param_id}; ip={self.ip}; port={self.port}; node={self.node_id}"
    # id = Column(Integer, primary_key=True, autoincrement=True)
    # name = Column(String(128), nullable=False)
    # model = Column(String(128), nullable=True)
    # mqtt_name = Column(String(64), nullable=False)
    # type_id = Column(Integer, ForeignKey("sensor_type.id"))
    # type = relationship("SensorType", back_populates="sensors")
    # tank_id = Column(Integer, ForeignKey("tank.id"))
    # tank = relationship("Tank", back_populates="sensors")
    # parameter_id = Column(Integer, ForeignKey("parameter.id"))
    # parameter = relationship("Parameter", back_populates="sensors")
    # checks = relationship("SensorCheck", back_populates="sensor")
    # logs = relationship("SensorLog", back_populates="sensor")
