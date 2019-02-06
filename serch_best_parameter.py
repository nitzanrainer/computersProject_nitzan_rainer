def search_best_parameter(filename):
    def clear_white_spaces(only_data):
        my_list = []
        big_list = []
        for a in only_data:
            for x in a:
                if x == '' or x == ' ':
                    continue
                else:
                    my_list.append(x)
            my_list1 = my_list.copy()
            my_list.clear()
            big_list.append(my_list1)
        return big_list

    def if_it_is_rows(new_data):  # make it rows
        if new_data[1][0] == 'x' or new_data[1][0] == 'y' or new_data[1][0] == 'dx' or new_data[1][0] == 'dy':
            return new_data
        else:
            fixed_str = [list(i) for i in zip(*new_data)]
            return fixed_str

    def check_list(data_list):
        if len(data_list[0]) == len(data_list[1]) == len(data_list[2]) == len(data_list[3]):
            for item in data_list:
                for letter in range(1, len(item)):
                    if item[letter] != '':
                        continue
                    else:
                        return 'Input file error: Data lists are not the same length.'
            return data_list
        else:
            return 'Input file error: Data lists are not the same length.'

    def from_list_to_dictionary(xin_row_data):
        mid_float_list = []
        data_dictionary = {}
        for lines in xin_row_data:
            for number in range(1, len(lines)):
                float_number = float(lines[number])
                mid_float_list.append(float_number)
                mid1_float_list = mid_float_list.copy()
            mid_float_list.clear()
            data_dictionary[lines[0]] = mid1_float_list
        return data_dictionary

    def check_uncertainties(data_dictionary):
        dx_values = data_dictionary.get('dx')
        dy_values = data_dictionary.get('dy')
        for dx in dx_values:
            if dx > 0:
                continue
            else:
                return 'Input file error: Not all uncertainties are positive.'
        for dy in dy_values:
            if dy > 0:
                continue
            else:
                return 'Input file error: Not all uncertainties are positive.'
        return data_dictionary

    def sqr_func(p):
        x_sqr_val = []
        for thing in p:
            x_sqr = thing ** 2
            x_sqr_val.append(x_sqr)
        return x_sqr_val

    def xy_func(x, y):
        xy_list = []
        for item in range(len(x)):
            new_xy = x[item] * y[item]
            xy_list.append(new_xy)
        return xy_list
    def list_for_a_b(a):
        new_a=[]
        if a[0]<a[1]:
            t=a[0]
            while t<a[1]:
                t=t+a[2]
                if t>a[1]:
                    return new_a
                else:
                    new_a.append(t)
            return new_a
        else:
            t=a[0]
            while t>a[1]:
                t=t+a[2]
                if t<a[1]:
                    return new_a
                else:
                    new_a.append(t)
            return new_a
    def chi2(y,x,a,b,dy):
        chi_sum=0
        for item in range(len(x)):
            chi2=((y[item]-(a*x[item]+b))/(dy[item]))*((y[item]-(a*x[item]+b))/(dy[item]))
            chi_sum=chi2+chi_sum
        return chi_sum
    def sqr_func(p):
        x_sqr_val=[]
        for thing in p :
            x_sqr=thing**2
            x_sqr_val.append(x_sqr)
        return x_sqr_val    
    def xy_func(x,y):
        xy_list=[]
        for item in range(len(x)):
            new_xy=x[item]*y[item]
            xy_list.append(new_xy)
        return xy_list
    def z_met(z, dy):
        up_sum = 0
        down_sum = 0
        for item in range (len(z)):
            up_z_met = z[item] / ((dy[item]) ** 2)
            up_sum = up_sum + up_z_met
        for item in range (len(dy)) :
            down_z_met = 1 / ((dy[item]) ** 2)
            down_sum = down_sum + down_z_met
        z = up_sum / down_sum
        return z     
    def new_x(x,a,b):
      x_for_line_list=[]
      for j in x:
            x_for_line=(j*a)+b
            x_for_line_list.append(x_for_line)
      return(x_for_line_list)
    from matplotlib import pyplot as plt
    new_data = []
    values_list = []
    only_data = []
    a_b_data=[]
    this_file = open(filename, 'r')
    data = this_file.readlines()
    for line in data:
      new_line =line.rstrip('\n') #remove'\n'
      lower_line=new_line.lower()
      new_data.append(lower_line)
    for number_of_row in range(0,len(new_data)-6):
      split_line=new_data[number_of_row].split(' ')
      #print(split_line)
      only_data.append(split_line)
    split_line2=new_data[-2].split(' ')
    only_data.append(split_line2)
    split_line1=new_data[-1].split(' ')
    #print (split_line1)
    only_data.append(split_line1)
    # print('this is only_data',  only_data)
    big_list = clear_white_spaces(only_data)  # out with the white spaces
    # print(big_list)
    in_row_data = if_it_is_rows(big_list)  # now data is in rows
    # print(in_row_data)
    if len(in_row_data) < 4:  # if there is a length problem in col
        return 'Input file error: Data lists are not the same length.'
    else:
        xin_row_data = check_list(in_row_data)  # if list has same length
        if type(xin_row_data) == str:
            return xin_row_data
        else:
            data_dictionary = from_list_to_dictionary(in_row_data)
            ok_data = check_uncertainties(data_dictionary)  # if there are any uncertainties
            if type(ok_data) == str:
                return ok_data
            else:
                #print(ok_data['a'])
                a_for_dictionary=list_for_a_b(ok_data['a'])
                ok_data['a']=a_for_dictionary
                b_for_dictionary=list_for_a_b(ok_data['b'])
                ok_data['b']=b_for_dictionary
                x = ok_data['x']
                y = ok_data['y']
                dx = ok_data['dx']
                dy = ok_data['dy']
                x_sqr=sqr_func(x)
                dy_sqr=sqr_func(dy)
                xy=xy_func(x,y)
                da2=(z_met((sqr_func(dy)),dy))/(len(x)*(z_met(x_sqr,dy)-((z_met(x,dy))**2)))
                da=da2**(0.5)
                db2=((z_met((sqr_func(dy)),dy))*(z_met(x_sqr,dy)))/(len(x)*(z_met(x_sqr,dy)-((z_met(x,dy))**2)))
                db=db2**(0.5)
                chi_list=[]
                a_b_list=[]
                big_list_a_b=[]
                for item_a in ok_data['a']:
                    for item_b in ok_data['b']:
                        new_chi2=chi2(y,x,item_a,item_b,dy)
                        chi_list.append(new_chi2)
                        a_b_list.append(item_a)
                        a_b_list.append(item_b)
                        copy_of=a_b_list[:]#makes copy of the list
                        a_b_list.clear()
                        big_list_a_b.append(copy_of)
                for item_b in ok_data['b']:
                    for item_a in ok_data['a']:
                        new_chi2=chi2(y,x,item_a,item_b,dy)
                        chi_list.append(new_chi2)
                        a_b_list.append(item_a)
                        a_b_list.append(item_b)
                        copy_of=a_b_list[:]#makes copy of the list
                        a_b_list.clear()
                        big_list_a_b.append(copy_of)
                chi2_p=min(chi_list)        
                index_for_a_b=chi_list.index(chi2_p)
                my_a_b=big_list_a_b[index_for_a_b]
                best_a=my_a_b[0]
                best_b=my_a_b[1]
                print('a=',best_a,'+-',da)
                print('b=',best_b,'+-',db)
                print('chi2=',chi2_p)
                chi2_list_for_chart=[]
                for item_a in ok_data['a']:
                    chi2_b=chi2(y,x,item_a,best_b,dy)
                    chi2_list_for_chart.append(chi2_b)
                p='a'
                q=str(best_b)
                t=('chi2(a,='+q)
                plt.plot(ok_data['a'],chi2_list_for_chart, 'b-')
                plt.ylabel(t.title())
                plt.xlabel(p.title())
                plt.show()
                plt.savefig('numeric_sampling', format='svg')
                        
                
                                              
                

                





