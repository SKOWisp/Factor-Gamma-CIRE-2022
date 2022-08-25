#!/usr/bin/env python3
# Román Tamez Vidal Tamayo Tamez

import rospy
import tf2_ros
import actionlib

from geometry_msgs.msg import PoseStamped, TransformStamped
from move_base_msgs.msg import MoveBaseGoal, MoveBaseAction

# Función para obtener información de la posición de la base del robot
def get_coords ():
    for i in range(10):   ###TF might be late, try 10 times
        try:
            trans = tfBuffer.lookup_transform('map', 'base_link', rospy.Time())
            return trans
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros. ExtrapolationException): 
            print ('Waiting for tf')
            trans = 0
            time.sleep(1)
            continue

# Cliente de navegación del robot                                                
navclient = actionlib.SimpleActionClient('/move_base/move', MoveBaseAction)

def move_base_goal(msg):
    
    print("--------Leyendo datos iniciales--------")
    # Imprimimos la info de la posición inicial y tiempo
    dataA = get_coords()
    timeA = dataA.header.stamp
    print("Tiempo inicial: ", timeA.to_sec())
    print("----Posición inicial:----")
    print(dataA.transform)
    print("----Meta:----")
    print(msg.pose)
    
    # Inicializamos un MoveBaseGoal
    goal = MoveBaseGoal()
    
    # Para trabajar con el sistema de referecia map
    goal.target_pose.header.frame_id = "map"  
    
    # Asignamos cada variable al objeto de meta
    goal.target_pose.pose.position.x = msg.pose.position.x
    goal.target_pose.pose.position.y = msg.pose.position.y
    goal.target_pose.pose.orientation = msg.pose.orientation
    
    # Enviamos la meta al cliente de navegación
    navclient.send_goal(goal)
    # Esperamos el resultado
    navclient.wait_for_result()
    state = navclient.get_state()
    
    if state == 3:
        print("Bien hecho")
        # Imprimimos la info de la posición final y tiempo
        dataB = get_coords()
        timeB = dataB.header.stamp
        timeTotal = timeB - timeA
        print("Tiempo final: ", timeB.to_sec())
        print("Tiempo total: ", timeTotal.to_sec())
        print("----Posición final:----")
        print(dataB.transform)
        
        # Salimos
        rospy.signal_shutdown("FIN")
    else:
        print("Algo salio mal")
    

TEAM = "Factor Gamma"
def main():
    print("EJERCICIO 02 - " + TEAM)
    rospy.init_node('stage02_navigation', anonymous=True, disable_signals=True)
                                  
    # Creamos un subscriptor para escuchar a /meta_competencia
    rospy.Subscriber('/meta_competencia', PoseStamped, move_base_goal)
    
    # Creamos buffer para realizar lecturas de tf
    global tfBuffer 
    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)
    
    rospy.spin()
    
if __name__ == "__main__":
    main()