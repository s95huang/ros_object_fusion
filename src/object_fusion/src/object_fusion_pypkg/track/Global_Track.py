from .Tracked_Object import Tracked_Object
from ..ros2python.Objects import Objects

class Global_Track():
    """docstring for Global_Track"""
    def __init__(self):
        super(Global_Track, self).__init__()
        self.tracked_objects = {}
        self.sensor_property = 0
        self.latest_object_id = 0
        self.classification_mass =0
        self.timestamp = 0 
        self.latest_id = 1 

    
    def add_object(self, fused_object:Objects,fusing_participants,timestamp,new_object = False):
        self.timestamp = timestamp   
        self.new_object = new_object
        if self.__contains__(fused_object.obj_id):
            self.tracked_objects[fused_object.obj_id].add_fused_object(fused_object,fusing_participants,timestamp)
        else:
            self.tracked_objects[fused_object.obj_id] = Fused_Object(fused_object,fused_object.obj_id,fusing_participants,timestamp)

    def create_new_global_object(self,fused_object:Objects,fusing_participants, timestamp ,new_object = False,classification_mass = 0):
        fused_object.fusion_id = self.latest_id
        self.tracked_objects[self.latest_id] = Fused_Object(fused_object,self.latest_id,fusing_participants,timestamp)
        self.tracked_objects[self.latest_id].current_fused_object.classification_mass = classification_mass 

        self.latest_id += 1

    def __contains__(self,item_id):
        return item_id in self.tracked_objects.keys()

    def __str__(self):
        string = f"Global Track with {len(self.tracked_objects.keys())} objects: {list(self.tracked_objects.keys())}"
        for tracked_objects in self.tracked_objects:
            string += f"\n Track  {self.tracked_objects[tracked_objects]}: {tracked_objects}"
        return string

    def to_ros_msg(self, ObjectsList, header):
        ros_msg = ObjectsList(header = header)
        
        for tracked_object in self.tracked_objects.values():
            ros_obj_msg = tracked_object.current_fused_object.to_ros_msg()
            ros_obj_msg.sensors_fused = tracked_object.fusing_participants
            ros_msg.obj_list.append(ros_obj_msg)

        return ros_msg

class Fused_Object(object):
    """docstring for Fused_Object"""
    def __init__(self,fused_object,_id,fusing_participants,timestamp):
        super(Fused_Object, self).__init__()
        self.timestamp = timestamp
        self.id = _id 
        self.current_fused_object = fused_object
        self.fusing_participants = fusing_participants
        self.sensors = []
        
    def __str__(self):        
        string = f"Fused Participants: {self.fusing_participants}"
        # string += f"current_fused_object Participants: f{self.fusing_participants}"
        return string

    def __repr__(self):        
        string = f"Fused Objects: Participants: {self.fusing_participants}"
        # string += f"current_fused_object Participants: f{self.fusing_participants}"
        return string

    def add_fused_object(self,fused_objects,fusing_participants:list,timestamp):
        for participants in fusing_participants:
            if not participants in self.fusing_participants:
                self.sensors.append(participants)
        self.timestamp = timestamp
        self.previous_object = self.current_fused_object
        self.current_fused_object = fused_objects
        self.fusing_participants = fusing_participants


        pass