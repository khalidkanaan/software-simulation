# from CLCG import CLCG
from newclcg import CLCG

def main():
    # lst = []
    # file_path = 'data/servinsp1.dat'
    # num_service_times = 300

    # seeds = [63868218, 923712]
    # params = [
    #     (40014, 0, 2147483563),
    #     (40692, 0, 2147483399)
    # ]
    # # params = [
    # #     (1664525, 1013904223, 2**32),
    # #     (69069, 0, 2**32)
    # # ]

    # clcg_instance = CLCG(file_path, num_service_times, seeds, params)

    # print(clcg_instance.std_dev)

    # print('Random Service Times:')
    # for _ in range(num_service_times):
    #    lst.append(clcg_instance.next())

    # print(lst)

    newclcg = CLCG()
    print(newclcg.calc_random_numbers())



if __name__ == '__main__':
    main()