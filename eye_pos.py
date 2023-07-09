import cv2 as cv
import numpy as np
import mediapipe as mp
import math
import utils


mp_face_mesh = mp.solutions.face_mesh
FONTS = cv.FONT_HERSHEY_COMPLEX
LEFT_EYE =[ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398]
RIGHT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246]

RIGHT_IRIS = [474, 475, 476, 477]

LEFT_IRIS = [469, 470, 471, 472]

L_H_LEFT = [33]  # right eye right most landmark
L_H_RIGHT = [133]  # right eye left most landmark
R_H_LEFT = [362]  # left eye right most landmark
R_H_RIGHT = [263]  # left eye left most landmark

def euclidean_dist(p_1, p_2):
    x_1, y_1 = p_1.ravel()
    x_2, y_2 = p_2.ravel()
    dist = math.sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2)
    return dist

def iris_pos(center, r_point, l_point, pos = ""):
    center_to_r_point_dist = euclidean_dist(center, r_point)
    dist_total = euclidean_dist(r_point, l_point)

    r = center_to_r_point_dist / dist_total

    if r < 0.42 or r == 0.42:
        pos = "right"
    elif r > 0.42 and (r< 0.57 or r ==0.57):
        pos = "center"
    else:
        pos = "left"
    return pos, r

def blinkRatio(img, landmarks, right_indices, left_indices):
    # Right eyes
    # horizontal line
    rh_right = landmarks[right_indices[0]]
    rh_left = landmarks[right_indices[8]]
    # vertical line
    rv_top = landmarks[right_indices[12]]
    rv_bottom = landmarks[right_indices[4]]
    # draw lines on right eyes
    cv.line(img, rh_right, rh_left, utils.GREEN, 2)
    cv.line(img, rv_top, rv_bottom, utils.WHITE, 2)

    # LEFT_EYE
    # horizontal line
    lh_right = landmarks[left_indices[0]]
    lh_left = landmarks[left_indices[8]]

    # vertical line
    lv_top = landmarks[left_indices[12]]
    lv_bottom = landmarks[left_indices[4]]

    cv.line(img, lh_right, lh_left, utils.GREEN, 2)
    cv.line(img, lv_top, lv_bottom, utils.WHITE, 2)

    rhDistance = euclidean_dist(rh_right, rh_left)
    rvDistance = euclidean_dist(rv_top, rv_bottom)

    lvDistance = euclidean_dist(lv_top, lv_bottom)
    lhDistance = euclidean_dist(lh_right, lh_left)

    reRatio = rhDistance / rvDistance
    leRatio = lhDistance / lvDistance

    ratio = (reRatio + leRatio) / 2
    return ratio







cap = cv.VideoCapture(0)

with mp_face_mesh.FaceMesh (
    max_num_faces= 2,
    refine_landmarks= True,
    min_detection_confidence= 0.5,
    min_tracking_confidence= 0.5
) as face_mech:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv.flip(frame, 1)
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        img_h, img_w = frame.shape[:2]
        res = face_mech.process(rgb_frame)
        if res.multi_face_landmarks:
            mesh_points =np.array([np.multiply([p.x, p.y ], [img_w, img_h]).astype(int) for p in res.multi_face_landmarks[0].landmark])
            b_ratio = blinkRatio(frame, mesh_points, RIGHT_EYE, LEFT_EYE)
            cv.putText(frame, f'ratio {round(b_ratio, 2)}', (100, 100), FONTS, 1.0, utils.GREEN, 2)
            if b_ratio > 5:
                cv.putText(frame, 'Blink', (200, 50), FONTS, 1.3, utils.PINK, 2)

            # print(mesh_points.shape)
            # cv.polylines(frame, [mesh_points[LEFT_EYE]], True, (0, 100, 0), 1, cv.LINE_AA)
            # cv.polylines(frame, [mesh_points[RIGHT_EYE]], True, (0, 100, 0), 1, cv.LINE_AA)
            cv.polylines(frame, [mesh_points[LEFT_IRIS]], True, (0, 100, 0), 1, cv.LINE_AA)
            cv.polylines(frame, [mesh_points[RIGHT_IRIS]], True, (0, 100, 0), 1, cv.LINE_AA)
            (cl_x, cl_y), l_radius = cv.minEnclosingCircle(mesh_points[LEFT_IRIS])
            (cr_x, cr_y), r_radius = cv.minEnclosingCircle(mesh_points[RIGHT_IRIS])

            left_center = np.array([cl_x, cl_y], dtype= np.int32)
            right_center = np.array([cr_x, cr_y], dtype= np.int32)
            cv.circle(frame, left_center, int(l_radius), (200, 0, 200), 1, cv.LINE_AA)
            cv.circle(frame, right_center, int(r_radius), (200, 0, 200), 1, cv.LINE_AA)
            cv.circle(frame, mesh_points[R_H_RIGHT][0], 3, (200, 200, 200), -1, cv.LINE_AA)
            cv.circle(frame, mesh_points[R_H_LEFT][0], 3, (0, 200, 200), -1, cv.LINE_AA)
            pos, r = iris_pos(right_center, mesh_points[R_H_RIGHT], mesh_points[R_H_LEFT][0])
            print(pos)
            cv.putText(frame,
                       f"dir: = {pos} {r:.2f}", (30, 30), cv.FONT_HERSHEY_PLAIN, 1.2, (0, 100, 0), 1, cv.LINE_AA)
        cv.imshow("image", frame)
        key = cv.waitKey(1)
        if key == ord("q"):
            break
cap.release()
cv.destroyAllWindows()
