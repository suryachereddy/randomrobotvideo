import robosuite as suite
from robosuite.controllers import load_controller_config
from robosuite.robots import Bimanual
import numpy as np
from robosuite.utils.input_utils import choose_environment,choose_robots

class render():
    
    def __init__(self,controller_name="JOINT_POSITION"):
        self.env="Lift"
        self.controller_name=controller_name
        self.controller_settings = {
        "OSC_POSE": [6, 6, 0.1],
        "OSC_POSITION": [3, 3, 0.1],
        "IK_POSE": [6, 6, 0.01],
        "JOINT_POSITION": [7, 7, 0.2],
        "JOINT_VELOCITY": [7, 7, -0.1],
        "JOINT_TORQUE": [7, 7, 0.25],
        }

        

        self.action_dim = self.controller_settings[controller_name][0]
        self.num_test_steps = self.controller_settings[controller_name][1]
        self.test_value = self.controller_settings[controller_name][2]


    def createenv(self,env="Lift",robots=None,controller_name="JOINT_POSITION",render=True):
        """
        This function will create the robot environment and set the controller

        Attributes:
            env (str): name of the environment. Default is "Lift"
            robots (list): list of robot names. Default is None
            controller_name (str): name of the controller. Default is "JOINT_POSITION"
            render (bool): if True, then it will render the environment.

        Returns:
            None
        
        TO DO:
            None
        """
        controller_config = load_controller_config(
            default_controller=controller_name)
        if render:
            print("Warning: Rendering is enabled in the simulator. This will not record the camera observation data")
            
            self.env = suite.make(
                env,
                # Use single arm env
                robots=["Jaco"],
                gripper_types="default",                # use default grippers per robot arm
                controller_configs=controller_config,   # each arm is controlled using OSCjoint_dim
                # (two-arm envs only) arms face each other
                #env_configuration="single-arm-opposed",
                has_renderer=True,                      # on-screen rendering
                render_camera="frontview",              # visualize the "frontview" camera
                camera_names="frontview",
                has_offscreen_renderer=False,           # no off-screen rendering
                control_freq=20,                        # 20 hz control for applied actions
                horizon=200,                            # each episode terminates after 200 steps
                use_object_obs=False,                   # no observations needed
                use_camera_obs=False,                   # no observations needed
            )
        else:
            self.env = suite.make(
                env,
                # Use single arm env
                robots=["Jaco"],
                gripper_types="default",                # use default grippers per robot arm
                controller_configs=controller_config,   # each arm is controlled using OSCjoint_dim
                # (two-arm envs only) arms face each other
                #env_configuration="single-arm-opposed",
                has_renderer=False,                      # on-screen rendering
                render_camera="frontview",              # visualize the "frontview" camera
                camera_names="frontview",
                has_offscreen_renderer=True,           # no off-screen rendering
                control_freq=20,                        # 20 hz control for applied actions
                horizon=200,                            # each episode terminates after 200 steps
                use_object_obs=False,                   # no observations needed
                use_camera_obs=True,                   # no observations needed
            )


    def randomAction(self,frames=120, save_path="!",render=True,debug=False):
        """
        This function will generate a random action and render the environment

        Attributes:
            frames (int): number of frames to render
            save_path (str): path to save the Numpy video array of. If "!", then it will not save the video. Also, please end the path with file name
            render (bool): if True, then it will render the environment. Note that this will not record the camera observation data
            debug (bool): Currently only used for developmen. Please ignore.

        Returns:
            None
        
        TO DO:
            - Allow to save robot's joint space along with frame
            - Allow side view camera
        """
        self.createenv(render=render)
        low, high = self.env.action_spec
        self.currentobs=None
        self.observation=[]
        for i in range(frames):
            action = np.random.uniform(low, high)
            obs, reward, done, _ = self.env.step(action)
            self.observation.append(obs)
            if render:
                self.env.render()
            if done:
                self.env.reset()
            if i==0 and debug:
                print(obs)
                print(obs.keys())
            self.currentobs=obs
        if save_path!="!":
            np.save(save_path,self.observation)