import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/ubuntu/rb3302_final_proj_code/student_ws/install/mapping_cartographer'
