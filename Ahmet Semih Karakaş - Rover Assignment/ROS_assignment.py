#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String


class DataRead():

    def callback(self, data):

        split_strings = []
        # The first and the Last character of the message
        if data.data[0] == "A" and data.data[-1] == "B":

            # Splitting the data
            datanew = data.data[1:-1]
            n = 4
            for index in range(0, len(datanew), n):
                split_strings.append(datanew[index: index + n])

            list_new = []

            # Changing the first character of subdata.
            for i in split_strings:
                s = list(i)

                if s[0] == "0":
                    s[0] = " "

                if s[0] == "1":
                    s[0] = "-"

                A = "".join(s)

                list_new.append(A)

            # Adjusting numbers above 255 and below -255
            list_int = []

            for j in list_new:
                list_int.append(int(j))

            list_int_new = []

            element = 0
            for element in range(len(list_int)):
                if list_int[element] < -255:
                    list_int_new.append(-255)

                elif list_int[element] > 255:
                    list_int_new.append(255)

                else:
                    list_int_new.append(list_int[element])
                element = element + 1

            # Converting to string
            list_new = []

            for i in list_int_new:
                list_new.append(str(i))

            data_final = ' '.join(list_new)
            rospy.loginfo(data_final)
            return data_final

    def __init__(self):
        rospy.init_node("Node_Arm_Drive", anonymous=False)
        rospy.Subscriber('/serial/robotic_arm', String, self.callback)
        rospy.Subscriber("/serial/drive", String, self.callback)
        pub_arm = rospy.Publisher(
            "/position/robotic_arm", String, queue_size=10)
        pub_drive = rospy.Publisher("/position/drive", String, queue_size=10)

        while not rospy.is_shutdown():
            pub_arm.publish(self.callback)
            pub_drive.publish(self.callback)
            # rate.sleep()
            rospy.spin()


if __name__ == '__main__':
    s = DataRead()
