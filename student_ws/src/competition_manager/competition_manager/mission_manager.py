import rclpy
from rclpy.node import Node

class mainLogic(Node):
    def __init__(self):
        super().__init__('mainLogic')


def main(args=None):
    rclpy.init(args=args)
    node = mainLogic()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
