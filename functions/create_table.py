def tablemaker(true, bias, sd):
    for i in range(12):
        bias[i] = round(bias[i], 2)
        sd[i] = round(sd[i], 2)

    print(f"""\\begin\u007bfigure\u007d[hbt!]
\centering
\caption\u007bWithout noise reduction: the bias and standard deviation\u007d
\label\u007btab:second\u007d
\\begin\u007btabular\u007d\u007b|c|c|c|c|l|\u007d

\hline
Number & Body part             & Value (cm)         & Bias (cm)                & Sigma (cm)\\\\ \hline
1      & chest, R\_shoulder    &           {true[0]}          &  {bias[0]}                      &   \multicolumn\u007b1\u007d\u007bc|\u007d\u007b{sd[0]}\u007d                \\\\  \hline
2      & R\_shoulder, R\_elbow &            {true[1]}            &   {bias[1]}                      &   \multicolumn\u007b1\u007d\u007bc|\u007d\u007b{sd[1]}\u007d                 \\\\ \hline
3      & R\_elbow, R\_hand     &             {true[2]}           &  {bias[2]}                      &   \multicolumn\u007b1\u007d\u007bc|\u007d\u007b{sd[2]}\u007d                       \\\\ \hline
4      & chest, L\_shoulder    &             {true[3]}          & {bias[3]}                      &   \multicolumn\u007b1\u007d\u007bc|\u007d\u007b{sd[3]}\u007d                   \\\\ \hline
5      & L\_shoulder, L\_elbow &              {true[4]}          & {bias[4]}                      &   \multicolumn\u007b1\u007d\u007bc|\u007d\u007b{sd[4]}\u007d                   \\\\ \hline
6      & L\_elbow, L\_hand     &            {true[5]}            &  {bias[5]}                      &   \multicolumn\u007b1\u007d\u007bc|\u007d\u007b{sd[5]}\u007d                        \\\\ \hline
7     & hip, R\_hip           &             {true[6]}           & {bias[6]}                      &   \multicolumn\u007b1\u007d\u007bc|\u007d\u007b{sd[6]}\u007d                  \\\\ \hline
8      & R\_hip, R\_knee       &             {true[7]}           & {bias[7]}                      &   \multicolumn\u007b1\u007d\u007bc|\u007d\u007b{sd[7]}\u007d                   \\\\ \hline
9     & R\_knee, R\_ankle     &             {true[8]}             &    {bias[8]}                      &   \multicolumn\u007b1\u007d\u007bc|\u007d\u007b{sd[8]}\u007d                 \\\\ \hline
10     & hip, L\_hip           &             {true[9]}          &   {bias[9]}                      &   \multicolumn\u007b1\u007d\u007bc|\u007d\u007b{sd[9]}\u007d             \\\\ \hline
11     & L\_hip, L\_knee       &            {true[10]}  &   {bias[10]}                      &   \multicolumn\u007b1\u007d\u007bc|\u007d\u007b{sd[10]}\u007d                 \\\\ \hline
12     & L\_knee, L\_ankle     &            {true[11]}  & {bias[11]}                      &   \multicolumn\u007b1\u007d\u007bc|\u007d\u007b{sd[11]}\u007d               \\\\ \hline
\end\u007btabular\u007d
\end\u007bfigure\u007d""")


truelist = [21,  # 'chest', 'R_shoulder'
            32,  # 'R_shoulder', 'R_elbow'
            32,  # 'R_elbow', 'R_hand'
            21,  # 'chest', 'L_shoulder'
            32,  # 'L_shoulder', 'L_elbow'
            32,  # L_elbow', 'L_hand'
            15,  # 'hip', 'R_hip'
            52,  # 'R_hip', 'R_knee'
            45,  # 'R_knee', 'R_ankle'
            15,  # 'hip', 'L_hip'
            52,  # 'L_hip', 'L_knee'
            45]  # 'L_knee', 'L_ankle'

# bias = [1.25163123, 0.44186726, 2.09700365, 2.38008663, 2.57179372, 0.13513358, 0.78040769, 3.33297123,
#         5.27755237, 6.51118335, 3.10641074, 2.52281621]
# sd = [0.9184849647053621, 1.4778536349262374, 1.2591833543943363, 1.450542729600326, 2.444565132632822,
#       1.3065449994642457, 1.5480188554475325, 1.6657809533033863, 3.333839104318101, 3.5122606368699962,
#       2.854792108560863, 2.476876054043504]
#bias = [1.25894166, 0.42469325, 2.16199272, 2.37083614, 2.58898053, 0.19654773,
# 0.76206497, 3.42670644, 5.24197998, 6.63503166, 3.15571255, 2.72730082]


if __name__ == "__main__":
    tablemaker(truelist, bias, sd)
