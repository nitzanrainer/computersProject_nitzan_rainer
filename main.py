def fit_linear(filename):
   def clear_white_spaces(only_data):
    my_list=[]
    big_list=[]
    for a in only_data:
        for x in a:
            if x=='' or x==' ':
                continue
            else:
                my_list.append(x)
        my_list1=my_list.copy()
        my_list.clear()    
        big_list.append(my_list1)          
    return big_list
   def if_it_is_rows(nd):#make it rows
      if nd[1][0] == 'x' or nd[1][0] == 'y' or nd[1][0] == 'dx' or nd[1][0] == 'dy':
         return nd
      else:
         fixed_str = [list(i) for i in zip(*nd)]
         return fixed_str
   def check_list(data_list): #check length
       if len(data_list[0])==len(data_list[1])==len(data_list[2])==len(data_list[3]):
           for item in data_list:
               for letter in range(1,len(item)):
                   if item[letter]!='':
                       continue
                   else:
                       return  'Input file error: Data lists are not the same length.'
           return data_list
       else:
           return  'Input file error: Data lists are not the same length.'
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
   def check_uncertainties(data_dictionary):###see if there are any uncertainties
       dx_values=data_dictionary.get('dx')
       dy_values=data_dictionary.get('dy')
       for dx in dx_values:
           if dx>0:
               continue
           else:
               return 'Input file error: Not all uncertainties are positive.'
       for dy in dy_values:
           if dy>0:
               continue
           else:
               return 'Input file error: Not all uncertainties are positive.'
       return data_dictionary  
    
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
   def z_met(z, dy):### average from insturctiomn (6)
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
   def chi2_func(a,b,x,dy,y):##calculate chi2
      chi2=0
      for item in range (len(x)):
            chi=((y[item]-(a*x[item]+b))/dy[item])**2
            chi2=chi+chi2
      return chi2
   def new_x(x,a,b):##y for plot
      x_for_line_list=[]
      for j in x:
            x_for_line=(j*a)+b
            x_for_line_list.append(x_for_line)
      return(x_for_line_list)
   def open_file(filename):
      this_file = open(filename, 'r')
      data = this_file.readlines() ##a list that every argument is a string of row
      this_file.close()
      return data

   from matplotlib import pyplot as plt #######the start of the function
   new_data = []
   values_list = []
   only_data = []
   data1=open_file(filename)
   for line in data1:
      new_line =line.rstrip('\n') #remove'\n'
      lower_line=new_line.lower()
      new_data.append(lower_line)
   for number_of_row in range(0,len(new_data)-3):  ###takes only the data without the axiss
      split_line=new_data[number_of_row].split(' ')
      only_data.append(split_line)
   big_list=clear_white_spaces(only_data)#out with the white spaces
   in_row_data=if_it_is_rows(big_list)# now data is in rows
   if len(in_row_data)<4: #if there is a length problem in col
      return'Input file error: Data lists are not the same length.'
   else:
      xin_row_data=check_list(in_row_data)#if list has same length
      if type(xin_row_data)==str:
         return xin_row_data
      else:
         data_dictionary=from_list_to_dictionary(in_row_data)
         ok_data=check_uncertainties(data_dictionary)  #if there are any uncertainties
         if type(ok_data)==str:
            return ok_data
         else:
            x=ok_data['x']
            y=ok_data['y']
            dx=ok_data['dx']
            dy=ok_data['dy']
            x_sqr=sqr_func(x)
            dy_sqr=sqr_func(dy)
            xy=xy_func(x,y)
            a=(z_met(xy,dy)-z_met(x,dy)*z_met(y,dy))/(z_met(x_sqr,dy)-((z_met(x,dy))**2))
            b=z_met(y,dy)-a*z_met(x,dy)
            da2=(z_met((sqr_func(dy)),dy))/(len(x)*(z_met(x_sqr,dy)-((z_met(x,dy))**2)))
            da=da2**(0.5)
            db2_up=((z_met(dy_sqr,dy))*(z_met(x_sqr,dy)))
            db2_down=(len(x)*(z_met(x_sqr,dy)-((z_met(x,dy))**2)))
            db2=db2_up/db2_down
            db=db2**(0.5)
            chi2=chi2_func(a,b,x,dy,y)
            chi2_reduced=chi2/(len(x)-2)
            print('a=',a,'+-',da)
            print('b=',b,'+-',db)
            print('chi2=',chi2)
            print('chi2_reducuced=',chi2_reduced)
            #print( (z_met(x_sqr,dy)))
            x_line=new_x(x,a,b)
            plt.plot(x,x_line,'r-')
            plt.errorbar(x,y,xerr=dx,yerr=dy,ecolor='blue',fmt='None')
            plt.ylabel(new_data[-1].title())
            plt.xlabel(new_data[-2].title())
            #plt.show()
            plt.savefig("linear_fit.svg")
            
            
