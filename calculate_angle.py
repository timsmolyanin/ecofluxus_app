from math import sqrt, sin


def calculate_angle(height, length, diameter, airexchange, troom, tout):
    """
    :return:
    """

    """ Constants """
    mlc = 1  # Minor Loss Coefficient
    angles = [90, 87, 84, 81, 78, 75, 72, 69, 66, 63, 60, 57, 54, 51, 48,
              45, 42, 39, 36, 33, 30, 27, 24, 21, 18,15, 12, 9, 6, 3, 0]

    """ Users Parameters """

    h = height
    L = length
    D = diameter
    q_set = airexchange
    # print(q_set)

    """ Data from temperature sensors """
    t_out = tout
    t_room = troom

    """ Calculated values """
    out_air_den = (1.293 * 273) / (273 + t_out)
    # print("out_air_den: ", out_air_den)
    room_air_den = (1.293 * 273) / (273 + t_room)
    # print("room_air_den: ", room_air_den)
    S = (D ** 2 * 3.1415) / 4
    # print("S: ", S)

    VD = list()
    V = list()
    q = list()
    try:
        for i in range(0, len(angles)):
            VD.append(sqrt((4 * (sin((angles[i] * 3.1415) / 180)) * S) / 3.1415))

            V.append(sqrt((2 * 9.81 * (out_air_den - room_air_den) * h) / (
                        (0.019 * L * room_air_den / VD[i]) + mlc * room_air_den)))

            q.append(V[i] * 3.1415 * (VD[i] ** 2 / 4) * 3600)
    except Exception as e:
        print(e)

    # print("VD: ", VD)
    # print("V: ", V)
    # print(q)

    a = get_nearest_value(q_set, q)
    return a[0], angles[a[1]]
    # print(a[0], angles[a[1]])


def get_nearest_value(n_value, n_list):
    try:
        list_of_difs = [abs(n_value - x) for x in n_list]
        result_index = list_of_difs.index(min(list_of_difs))

        return n_list[result_index], result_index
    except:
        print("valksnsa")


if __name__ == "__main__":
    h = 6
    L = 7.5
    D_vent = 0.116470849
    S_vent = 0.0106
    air_exch = 30
    tin = 25
    tout = -50
    res = calculate_angle(h, L, D_vent, air_exch, tin, tout)
    print(res)

