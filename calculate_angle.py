from math import sqrt, sin
import cmath


def calculate_angle(height, length, diameter, airexchange, troom, tout):
    """
    :return:
    """

    """ Constants """
    MLC = 1  # Minor Loss Coefficient
    ANGLES = [90, 87, 84, 81, 78, 75, 72, 69, 66, 63, 60, 57, 54, 51, 48,
              45, 42, 39, 36, 33, 30, 27, 24, 21, 18,15, 12, 9, 6, 3, 0]

    """ Users Parameters """
    h = height
    L = length
    D = diameter
    q_set = airexchange
    # print(height, length, diameter, airexchange)

    """ Data from temperature sensors """
    t_out = tout
    t_room = troom

    """ Calculated values """
    out_air_den = (1.293 * 273) / (273 + t_out)
    room_air_den = (1.293 * 273) / (273 + t_room)
    S = (D ** 2 * 3.1415) / 4

    VD = list()
    V = list()
    q = list()
    try:
        for angle in ANGLES:
            tmp_val = sqrt((4 * (sin((angle * 3.1415) / 180)) * S) / 3.1415)
            if tmp_val != 0:
                VD.append(tmp_val)
        # print("VD = ", VD)
        for v in VD:
            tmpv1 = 2 * 9.81 * (out_air_den - room_air_den) * h
            # print("tmp1 = ", tmpv1)
            tmpv2 = 0.019 * L * room_air_den / v
            # print("tmp2 = ", tmpv2)
            tmpv3 = MLC * room_air_den
            # print("tmp3 = ", tmpv3)
            V.append(cmath.sqrt(tmpv1 / (tmpv2 + tmpv3)))
        # print("V = ", V)
        for i in range(len(VD)):
            q.append(V[i] * 3.1415 * (VD[i] ** 2 / 4) * 3600)
    except Exception as err:
        print(err)

    # print(q_set, q)
    air_exch = get_nearest_value(q_set, q)
    air_exch_calc = air_exch[0].real
    return round(air_exch_calc, 1), ANGLES[air_exch[1]]

def get_nearest_value(n_value, n_list):
    try:
        list_of_difs = [abs(n_value - x) for x in n_list]
        result_index = list_of_difs.index(min(list_of_difs))

        return n_list[result_index], result_index
    except Exception as err:
        print(err)


if __name__ == "__main__":
    h = 6
    L = 7.5
    D_vent = 0.125
    S_vent = 1
    air_exch = 30
    tin = 25
    # for tout in range(25):
    res = calculate_angle(h, L, D_vent, air_exch, tin, 22)
    print(res)

