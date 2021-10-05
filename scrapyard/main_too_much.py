#
#     {"version": 1.3, "people": [{"person_id": [-1],
#                                  "pose_keypoints_2d":
#                                  [  219.676, 46.4492, 0.866838, NOSE
#                                     235.565, 118.979, 0.912748, CHEST
#                                     177.219,131.278, 0.806771,  RSHOULDER
#                                     166.627, 224.971, 0.813453, RELBOW
#                                     163.074, 311.624, 0.864266, RHAND
#                                     292.159, 108.308, 0.850031, LSHOULDER
#                                     332.788, 187.854, 0.862748, LELBOW
#                                     373.408, 260.358, 0.823099, LHAND
#                                     262.04, 272.655, 0.754014,  HIP
#                                     230.21, 276.201, 0.70194,   RHIP
#                                     217.856, 398.227, 0.733951, RKNEE
#                                     203.725, 534.272,0.646246,  RANKLE
#                                     293.909, 267.42, 0.721418,  LHIP
#                                     286.86, 364.595, 0.708921,
#                                     277.965, 419.399, 0.831686,
#                                     205.58, 35.8069, 0.876099,
#                                     230.291,32.3268, 0.906395,
#                                     191.346, 42.968, 0.787619,
#                                     247.969, 35.8283,0.869093,
#                                     277.966, 449.476, 0.829238,
#                                     290.348, 445.937, 0.81065,
#                                     272.65, 417.673, 0.62363,
#                                     212.573, 576.69, 0.52354,
#                                     198.474,573.212, 0.491662,
#                                     202.013, 539.625, 0.350447],
#                                  "face_keypoints_2d": [], "hand_left_keypoints_2d": [], "hand_right_keypoints_2d": [],
#                                  "pose_keypoints_3d": [], "face_keypoints_3d": [], "hand_left_keypoints_3d": [],
#                                  "hand_right_keypoints_3d": []}]}
# """
#     #
#     # # nose_x, nose_y, nose_z = ff[0][0], ff[0][1], ff[0][2]
#     # nose = (ff[0][0], ff[0][1], ff[0][2])
#     # # chest_x, chest_y, chest_z = ff[1][0], ff[1][1], ff[1][2]
#     # chest = (ff[1][0], ff[1][1], ff[1][2])
#     # # R_shoulder_x, R_shoulder_y, R_shoulder_z = ff[2][0], ff[2][1], ff[2][2]
#     # R_shoulder = (ff[2][0], ff[2][1], ff[2][2])
#     # # R_elbow_x, R_elbow_y, R_elbow_z = ff[3][0], ff[3][1], ff[3][2]
#     # R_elbow = (ff[3][0], ff[3][1], ff[3][2])
#     # # R_hand_x, R_hand_y, R_hand_z = ff[4][0], ff[4][1], ff[4][2]
#     # R_hand = (ff[4][0], ff[4][1], ff[4][2])
#     # # L_shoulder_x, L_shoulder_y, L_shoulder_z = ff[5][0], ff[5][1], ff[5][2]
#     # L_shoulder = (ff[5][0], ff[5][1], ff[5][2])
#     # # L_elbow_x, L_elbow_y, L_elbow_z = ff[6][0], ff[6][1], ff[6][2]
#     # L_elbow = (ff[6][0], ff[6][1], ff[6][2])
    # # L_hand_x, L_hand_y, L_hand_z = ff[7][0], ff[7][1], ff[7][2]
    # L_hand = (ff[7][0], ff[7][1], ff[7][2])
    # # hip_x, hip_y, hip_z = ff[8][0], ff[8][1], ff[8][2]
    # hip = (ff[8][0], ff[8][1], ff[8][2])
    # # R_hip_x, R_hip_y, R_hip_z = ff[9][0], ff[9][1], ff[9][2]
    # R_hip = (ff[9][0], ff[9][1], ff[9][2])
    # # R_knee_x, R_knee_y, R_knee_z = ff[10][0], ff[10][1], ff[10][2]
    # R_knee = (ff[10][0], ff[10][1], ff[10][2])
    # # R_ankle_x, R_ankle_y, R_ankle_z = ff[11][0], ff[11][1], ff[11][2]
    # R_ankle = (ff[11][0], ff[11][1], ff[11][2])
    # # L_hip_x, L_hip_y, L_hip_z = ff[12][0], ff[12][1], ff[12][2]
    # L_hip = (ff[12][0], ff[12][1], ff[12][2])
    # # L_knee_x, L_knee_y, L_knee_z = ff[13][0], ff[13][1], ff[13][2]
    # L_knee = (ff[13][0], ff[13][1], ff[13][2])
    # # L_ankle_x, L_ankle_y, L_ankle_z = ff[14][0], ff[14][1], ff[14][2]
    # L_ankle = (ff[14][0], ff[14][1], ff[14][2])
    # # R_eye_x, R_eye_y, R_eye_z = ff[15][0], ff[15][1], ff[15][2]
    # R_eye = (ff[15][0], ff[15][1], ff[15][2])
    # # L_eye_x, L_eye_y, L_eye_z = ff[16][0], ff[16][1], ff[16][2]
    # L_eye = (ff[16][0], ff[16][1], ff[16][2])
    # # R_ear_x, R_ear_y, R_ear_z = ff[17][0], ff[17][1], ff[17][2]
    # R_ear = (ff[17][0], ff[17][1], ff[17][2])
    # # L_ear_x, L_ear_y, L_ear_z = ff[18][0], ff[18][1], ff[18][2]
    # L_ear = (ff[18][0], ff[18][1], ff[18][2])
    # # L_foot2_x, L_foot2_y, L_foot2_z = ff[19][0], ff[19][1], ff[19][2]
    # L_foot2 = (ff[19][0], ff[19][1], ff[19][2])
    # # L_foot3_x, L_foot3_y, L_foot3_z = ff[20][0], ff[20][1], ff[20][2]
    # L_foot3 = (ff[20][0], ff[20][1], ff[20][2])
    # # L_foot4_x, L_foot4_y, L_foot4_z = ff[21][0], ff[21][1], ff[21][2]
    # L_foot4 = (ff[21][0], ff[21][1], ff[21][2])
    # # R_foot2_x, R_foot2_y, R_foot2_z = ff[22][0], ff[22][1], ff[22][2]
    # R_foot2 = (ff[22][0], ff[22][1], ff[22][2])
    # # R_foot3_x, R_foot3_y, R_foot3_z = ff[23][0], ff[23][1], ff[23][2]
    # R_foot3 = (ff[23][0], ff[23][1], ff[23][2])
    # # R_foot4_x, R_foot4_y, R_foot4_z = ff[24][0], ff[24][1], ff[24][2]
    # R_foot4 = (ff[24][0], ff[24][1], ff[24][2])
    #
    # table = [['Number', 'Part of the body', 'x', 'y', 'z'],
    #          [0, 'nose', nose],
    #          [1, 'chest', chest],
    #          [2, 'R shoulder', R_shoulder],
    #          [3, 'R elbow', R_elbow],
    #          [4, 'R hand', R_hand],
    #          [5, 'l shoulder', L_shoulder],
    #          [6, 'l elbow ', L_elbow],
    #          [7, 'l hand', L_hand],
    #          [8, 'hip', hip],
    #          [9, 'R hip', R_hip],
    #          [10, 'R knee', R_knee],
    #          [11, 'R ankle', R_ankle],
    #          [12, 'l hip', L_hip],
    #          [13, 'l knee', L_knee],
    #          [14, 'l ankle', L_ankle],
    #          [15, 'R eye', R_eye],
    #          [16, 'l eye', L_eye],
    #          [17, 'R ear', R_ear],
    #          [18, 'l ear', L_ear],
    #          [19, 'l foot-2', L_foot2],
    #          [20, 'l foot-3', L_foot3],
    #          [21, 'l foot-4', L_foot4],
    #          [22, 'R foot-2', R_foot2],
    #          [23, 'R foot-3', R_foot3],
    #          [24, 'R foot-4', R_foot4]]
    #
    # # print(tabulate(table))
    #
    #
    #      myfont = cv2.FONT_HERSHEY_SIMPLEX
    #      fontscale = 0.75
    #      fontthickness = 2
    #      textpos = (447, 40)
    #      tx1, ty1 = textpos
    #      twidht, theight = cv2.getTextSize("hip-anke length:", myfont, fontscale, fontthickness)
    #      cv2.putText(myim_copy, "hip-ankle length:", textpos, myfont, fontscale, (255, 0, 0), fontthickness)
    #      tx2 = tx1 + 3 * theight
    #   # print(theight)
    #      textpos2 = (447, 70)
    #      textpos3 = (447, 100)
    #      cv2.putText(myim_copy, f"{dist}", textpos2, myfont, fontscale, (255, 0, 0), fontthickness)
    #      cv2.putText(myim_copy, f"real = 97", textpos3, myfont, fontscale, (0, 0, 0), fontthickness)
