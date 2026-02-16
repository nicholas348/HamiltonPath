from manim import *



class HamiltonPath(Scene):
    def construct(self) :
        #setting dots
        dot_pos_list = [
            [3.8378238140915517, -0.5733057553287386],#0
            [3.9094422441839445, -1.50972436618488],#1
            [1.22728219167647, 2.8840997591867765],#2
            [- 0.9014937142731325, -2.886678029017851],#3
            [- 4.4408807914835835, 0.38928870636404467],#4





            [- 1.5190050841020142, -0.555995671348672],#5
            [1.87625422654442, 1.3674150662044973],#6
            [3.355581091063108, 2.8278229998944537],#7
            [2.144193665966549, -2.8786121097563795],#8
            [-1.6778929303556458, 0.9683144634387277],#9
            [-2.467284852119872, -0.2263938676336097],#10
            [-4.09644323847631, -1.0267798936875705],#11
            [0.13104734778506, 1.2031149280588904],#12
            [2.477545942167559, 0.582829322973079],#13
            [0.7878419899872489, 0.7838878005782175],#14
            [-4.611300071071119, 0.6147144346102609],#15
        ]
        dot_label = VGroup(
            [Text(str(i)).move_to(RIGHT*dot_pos_list[i][0]+UP*dot_pos_list[i][1]) for i in range(len(dot_pos_list))]
        )
        line_list = [
            [0,1],
            [1,2],
            [2,3],
            [3,0],
            [2,4],
            [3,4]




        ]

        def get_index(u,v):
            try:
                return line_list.index([u, v])
            except ValueError:
                return line_list.index([v, u])


        dots = VGroup(
            *[Dot(point=RIGHT*dot_pos_list[i][0]+UP*dot_pos_list[i][1]) for i in range(len(dot_pos_list))]
        )
        lines = VGroup(
            *[Line(dots[line_list[i][0]], dots[line_list[i][1]]) for i in range(len(line_list))]

        )
        self.add(dots[0:4],lines,dot_label)
        first_path_list = [0,1,2,3,4]
        second_path_list = [4,3,0,1,2]
        third_path_list = [3,4,2,3,0,1,2]
        for i in range(len(first_path_list) - 1):
            u = first_path_list[i]
            v = first_path_list[i + 1]

            # 4. ROBUST LOGIC: Check both [u,v] and [v,u]
            # This prevents crashing if the path goes "backwards"
            try:
                line_index = line_list.index([u, v])
            except ValueError:
                line_index = line_list.index([v, u])

            self.play(
                lines[line_index].animate.set_color(YELLOW),
                dots[u].animate.set_color(YELLOW),
                # If it's the last step, color the final dot too
                dots[v].animate.set_color(YELLOW) ,
                run_time=0.5
            )
        self.play(
            *[dots[m].animate.set_color(RED) for m in range(len(first_path_list))],
            *[lines[

                  line_list.index(
                      [first_path_list[m],
                       first_path_list[m + 1]
                       ]
                  )
              ].animate.set_color(RED) for m in range(len(first_path_list) - 1)
              ]
        )
        self.play(
            dots[0:5].animate.set_color(WHITE),
            lines.animate.set_color(WHITE),
            run_time=0.5
        )



        for i in range(len(second_path_list) - 1):
            u = second_path_list[i]
            v = second_path_list[i + 1]

            # 4. ROBUST LOGIC: Check both [u,v] and [v,u]
            # This prevents crashing if the path goes "backwards"
            try:
                line_index = line_list.index([u, v])
            except ValueError:
                line_index = line_list.index([v, u])

            self.play(
                lines[line_index].animate.set_color(YELLOW),
                dots[u].animate.set_color(YELLOW),
                # If it's the last step, color the final dot too
                dots[v].animate.set_color(YELLOW) ,
                run_time=0.5
            )
        self.play(
            *[dots[m].animate.set_color(RED) for m in range(len(second_path_list))],
            *[lines[
                 get_index(
                     second_path_list[m],
                     second_path_list[m+1]

                )
                ].animate.set_color(RED) for m in range(len(second_path_list) - 1)
            ]
        )


        self.play(
            dots[0:5].animate.set_color(WHITE),
            lines.animate.set_color(WHITE),
            run_time=0.5
        )
        for i in range(len(third_path_list) - 1):
            u = third_path_list[i]
            v = third_path_list[i + 1]

            # 4. ROBUST LOGIC: Check both [u,v] and [v,u]
            # This prevents crashing if the path goes "backwards"
            try:
                line_index = line_list.index([u, v])
            except ValueError:
                line_index = line_list.index([v, u])

            self.play(
                lines[line_index].animate.set_color(YELLOW),
                dots[u].animate.set_color(YELLOW),
                # If it's the last step, color the final dot too
                dots[v].animate.set_color(YELLOW) ,
                run_time=0.5
            )
            self.wait(1)
        self.play(
            dots[0:5].animate.set_color(GREEN),
            lines.animate.set_color(GREEN),
            run_time=0.5
        )
        self.play(
            dots[0:5].animate.set_color(WHITE),
            lines.animate.set_color(WHITE),
            run_time=0.5
        )

        self.wait(2)


        #hamilton path
        first_hamilton_path = [3,2,1,0]
        second_hamilton_path = [3,2,4]
        third_hamilton_path = [3,4,2,1,0,3]



        for i in range(len(first_hamilton_path) - 1):
            u = first_hamilton_path[i]
            v = first_hamilton_path[i + 1]

            # 4. ROBUST LOGIC: Check both [u,v] and [v,u]
            # This prevents crashing if the path goes "backwards"
            line_index = get_index(u,v)

            self.play(
                lines[line_index].animate.set_color(YELLOW),
                dots[u].animate.set_color(YELLOW),
                # If it's the last step, color the final dot too
                dots[v].animate.set_color(YELLOW) ,
                run_time=0.5
            )
            self.wait(1)
        self.play(
            *[dots[m].animate.set_color(RED) for m in first_hamilton_path],
            *[lines[
                  get_index(
                      first_hamilton_path[m],
                      first_hamilton_path[m + 1]

                  )
              ].animate.set_color(RED) for m in range(len(first_hamilton_path) - 1)
              ]
        )

        self.play(
            dots[0:5].animate.set_color(WHITE),
            lines.animate.set_color(WHITE),
            run_time=0.5
        )

        self.wait(1)


        for i in range(len(second_hamilton_path) - 1):
            u = second_hamilton_path[i]
            v = second_hamilton_path[i + 1]

            # 4. ROBUST LOGIC: Check both [u,v] and [v,u]
            # This prevents crashing if the path goes "backwards"
            line_index = get_index(u,v)

            self.play(
                lines[line_index].animate.set_color(YELLOW),
                dots[u].animate.set_color(YELLOW),
                # If it's the last step, color the final dot too
                dots[v].animate.set_color(YELLOW) ,
                run_time=0.5
            )
            self.wait(1)
        self.play(
            *[dots[m].animate.set_color(RED) for m in second_hamilton_path],
            *[lines[
                  get_index(
                      second_hamilton_path[m],
                      second_hamilton_path[m + 1]

                  )
              ].animate.set_color(RED) for m in range(len(second_hamilton_path) - 1)
              ]
        )

        self.play(
            dots[0:5].animate.set_color(WHITE),
            lines.animate.set_color(WHITE),
            run_time=0.5
        )

        self.wait(1)

        for i in range(len(third_hamilton_path) - 1):
            u = third_hamilton_path[i]
            v = third_hamilton_path[i + 1]

            # 4. ROBUST LOGIC: Check both [u,v] and [v,u]
            # This prevents crashing if the path goes "backwards"
            line_index = get_index(u,v)

            self.play(
                lines[line_index].animate.set_color(YELLOW),
                dots[u].animate.set_color(YELLOW),
                # If it's the last step, color the final dot too
                dots[v].animate.set_color(YELLOW) ,
                run_time=0.5
            )
            self.wait(1)
        self.play(
            dots[0:5].animate.set_color(GREEN) ,
            *[lines[
                  get_index(
                      third_hamilton_path[m],
                      third_hamilton_path[m + 1]

                  )
              ].animate.set_color(GREEN) for m in range(len(third_hamilton_path) - 1)
              ]
        )

        self.play(
            dots[0:5].animate.set_color(WHITE),
            lines.animate.set_color(WHITE),
            run_time=0.5
        )

        self.wait(1)


        extended_line_list = [
            [3,14],
            [3,5],
            [15,10],
            [15,9],
            [11,5],
            [8,13],
            [13,11],
            [6,7],
            [8,14],
            [9,3],
            [9,7],
            [10,12],
            [12,6],
            [6,13],
            [3,11],
            [12,14],
            [10,5]
        ]
        tot_line = line_list + extended_line_list
        def get_index(u,v):
            try:
                return tot_line.index([u, v])
            except ValueError:
                return tot_line.index([v, u])

        extended_lines = VGroup(
            *[
                Line(dots[i[0]], dots[i[1]]) for i in extended_line_list
            ]
        )
        tot_lines = VGroup(*lines, *extended_lines)
        self.play(
            FadeIn(extended_lines),
            FadeIn(dots[5:]),
            run_time=2
        )
        self.wait(10)
        first_long_non_hamilton = [3,14,8,13,6,7,9,15,10,5,11]
        second_long_non_hamilton = [0,1,2,3,11,5]
        for i in range(len(first_long_non_hamilton) - 1):
            u = first_long_non_hamilton[i]
            v = first_long_non_hamilton[i + 1]

            # 4. ROBUST LOGIC: Check both [u,v] and [v,u]
            # This prevents crashing if the path goes "backwards"
            line_index = get_index(u,v)

            self.play(
                tot_lines[line_index].animate.set_color(YELLOW),
                dots[u].animate.set_color(YELLOW),
                # If it's the last step, color the final dot too
                dots[v].animate.set_color(YELLOW) ,
                run_time=0.5
            )
        self.play(
            *[dots[m].animate.set_color(RED) for m in first_long_non_hamilton],
            *[tot_lines[
                  get_index(
                      first_long_non_hamilton[m],
                      first_long_non_hamilton[m + 1]

                  )
              ].animate.set_color(RED) for m in range(len(first_long_non_hamilton) - 1)
              ]
        )

        self.play(
            dots.animate.set_color(WHITE),
            tot_lines.animate.set_color(WHITE),
            run_time=0.5
        )



        for i in range(len(second_long_non_hamilton) - 1):
            u = second_long_non_hamilton[i]
            v = second_long_non_hamilton[i + 1]

            # 4. ROBUST LOGIC: Check both [u,v] and [v,u]
            # This prevents crashing if the path goes "backwards"
            line_index = get_index(u,v)

            self.play(
                tot_lines[line_index].animate.set_color(YELLOW),
                dots[u].animate.set_color(YELLOW),
                # If it's the last step, color the final dot too
                dots[v].animate.set_color(YELLOW) ,
                run_time=0.5
            )
        self.play(
            *[dots[m].animate.set_color(RED) for m in second_long_non_hamilton],
            *[tot_lines[
                  get_index(
                      second_long_non_hamilton[m],
                      second_long_non_hamilton[m + 1]

                  )
              ].animate.set_color(RED) for m in range(len(second_long_non_hamilton) - 1)
              ]
        )

        self.play(
            dots.animate.set_color(WHITE),
            tot_lines.animate.set_color(WHITE),
            run_time=0.5
        )
        n_p = Text("NP").shift(RIGHT*6)
        self.play(Write(n_p))

        hamilton_path = [4, 2, 1, 0, 3, 11, 13, 8, 14, 12, 6, 7, 9, 15, 10, 5]
        for i in range(len(hamilton_path) - 1):
            u = hamilton_path[i]
            v = hamilton_path[i + 1]

            # 4. ROBUST LOGIC: Check both [u,v] and [v,u]
            # This prevents crashing if the path goes "backwards"
            line_index = get_index(u,v)

            self.play(
                tot_lines[line_index].animate.set_color(YELLOW),
                dots[u].animate.set_color(YELLOW),
                # If it's the last step, color the final dot too
                dots[v].animate.set_color(YELLOW) ,
                run_time=0.5
            )
        self.play(
            *[dots[m].animate.set_color(GREEN) for m in hamilton_path],
            *[tot_lines[
                  get_index(
                      hamilton_path[m],
                      hamilton_path[m + 1]

                  )
              ].animate.set_color(GREEN) for m in range(len(hamilton_path) - 1)
              ]
        )

        self.play(
            dots.animate.set_color(WHITE),
            tot_lines.animate.set_color(WHITE),
            run_time=0.5
        )

        p = Text("P").shift(LEFT*6)
        self.play(Write(p))
        P_equal_NP =VGroup(
            MathTex("P"),
            MathTex("="),
            MathTex(" NP")
        ).arrange(RIGHT).scale(2)
        self.play(
            ReplacementTransform(p,P_equal_NP[0]),
            ReplacementTransform(n_p,P_equal_NP[2]),
            ReplacementTransform(VGroup(tot_lines,dots),P_equal_NP[1])
        )
        big_question_mark = MathTex("?",color=RED).scale(4)
        self.play(Write(big_question_mark))




















