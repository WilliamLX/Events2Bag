#!/usr/bin/env python
import roslib;

import rospy
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats

from metavision_core.event_io import EventsIterator
from metavision_sdk_core import PeriodicFrameGenerationAlgorithm
from metavision_sdk_ui import EventLoop, BaseWindow, Window, UIAction, UIKeyEvent

import numpy


accumulation_time_us = 10000


def events_publisher():

    # ros init
    pub = rospy.Publisher('events', numpy_msg(Floats))
    rospy.init_node('events_publisher', anonymous=True)
    r = rospy.Rate(10)

    # events init
    # Events iterator on Camera or RAW file
    mv_iterator = EventsIterator(input_path="", delta_t=1e3)
    height, width = mv_iterator.get_size()  # Camera Geometry
    print(height, width)

    # while not rospy.is_shutdown():
    #     print(height,width)
    #     a = numpy.array([1.0,2.1,3.2,4.3,5.4,6.5],dtype=numpy.float32)
    #     pub.publish(a)
    #     r.sleep()
    # count = 0

    # for evs in mv_iterator:
    #     # print(type(evs))
    #     # ei = evs[0]
    #     # print(ei)
    #     # print(type(evs))
    #     count += 1
    #     print(count)
    #     # print(evs)
    #     # a = numpy.array(evs,dtype=numpy.float32)

    #     # a = numpy.array([1.0],dtype=numpy.float32)
    #     pub.publish(evs)
    #     r.sleep()
    #     # exit(0)


    with Window(title="Metavision SDK Get Started", width=width, height=height, mode=BaseWindow.RenderMode.BGR) as window:
        def keyboard_cb(key, scancode, action, mods):
            if action != UIAction.RELEASE:
                return
            if key == UIKeyEvent.KEY_ESCAPE or key == UIKeyEvent.KEY_Q:
                window.set_close_flag()

        window.set_keyboard_callback(keyboard_cb)

        # Event Frame Generator
        event_frame_gen = PeriodicFrameGenerationAlgorithm(width, height, accumulation_time_us)

        def on_cd_frame_cb(ts, cd_frame):
            window.show(cd_frame)

        event_frame_gen.set_output_callback(on_cd_frame_cb)

        # Process events
        for evs in mv_iterator:
            # print(evs)
            # Dispatch system events to the window
            EventLoop.poll_and_dispatch()

            event_frame_gen.process_events(evs)
            pub.publish(evs)

            # a = numpy.array([1.0,2.1,3.2,4.3,5.4,6.5],dtype=numpy.float32)
            # pub.publish(a)
            if window.should_close():
                break
            # r.sleep()



if __name__ == '__main__':
    events_publisher()




# # accumulation_time_us = 10000

#     # Events iterator on Camera or RAW file
#     mv_iterator = EventsIterator(input_path=args.input_path, delta_t=1e3)
#     height, width = mv_iterator.get_size()  # Camera Geometry

#     print(height, width)
