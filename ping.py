import subprocess 

def ping(destination, ip_version=4, num_tries=1, timeout=1, encoding="utf-8"):
    '''
        Performs a ping to 'destination', with version 'ip_version' of IP
        Tries 'num_tries' times, with a timeout of 'timeout'. 
        Extracts the result with 'encoding' 

        Returns: 
            [packet, rtt, error]
            packet = transmitted, received, loss, time, time unit
            rtt = min, max, avg, mdev, time unit
    '''

    # Defining command
    if ip_version == 4: 
        command = "ping {} -c {} -W {}".format(destination, num_tries, timeout)
    else: 
        command = "ping6 {} -c {} -W {}".format(destination, num_tries, timeout)

    # Executing command
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p_out, p_err = p.communicate()
    p_code = p.returncode
    p_out, p_err = p_out.decode(encoding), p_err.decode(encoding)

    # Formatting output
    error = "" 
    rtt = [0, 0, 0, 0, '']
    packets = [0, 0, 0, 0]

    if p_code != 0: 
        error = p_err
    else: 
        lines = p_out.split("\n") 
        rtt_line = (lines[-2]).split(' ') 
        rtt = list(map(float, rtt_line[-2].split('/'))) + [rtt_line[-1]]
        pack_line = (lines[-3]).split(' ')
        packets = [float(pack_line[0]), float(pack_line[3]), pack_line[5], pack_line[-1]]


    return [packets, rtt, error]

