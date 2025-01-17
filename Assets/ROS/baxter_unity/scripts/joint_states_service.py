#!/usr/bin/env python  
import rospy
from rospy.exceptions import ROSException

from sensor_msgs.msg import JointState
from baxter_unity.srv import JointStateService, JointStateServiceRequest, JointStateServiceResponse

def get_joint_states(req):

    response = JointStateServiceResponse()
    try:
        joint_state_msg = rospy.wait_for_message("robot/joint_states", JointState, timeout=3.0)
        while len(joint_state_msg.position) < 2:
            joint_state_msg = rospy.wait_for_message("robot/joint_states", JointState)

        response.joint_state_msg = joint_state_msg
        return response
    except ROSException:
        # Fixed starting position in case real robot is not connected
        response.joint_state_msg.position = [0, 0, -1.2, 1.9, 0, -1, 0.67, 1.03, -0.5, 1.2, 1.9, 0, -1, -0.67, 1.03, 0.5, 0]
        return response

if __name__ == '__main__':

    rospy.init_node('baxter_joint_states_service')
    s = rospy.Service('baxter_joint_states', JointStateService, get_joint_states)
    rospy.spin()
