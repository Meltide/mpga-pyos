from cmdList.registerCmd import registerCmd
import datetime, calendar #时间日期库

def calendar(self):
    self.error = 0
    today = datetime.datetime.today()
    yy = str(today.year)  # int(input("Year: "))
    mm = str(today.month)  # int(input("Month: "))
    dd = str(today.day)
    print(f"Now: {Fore.BLUE}{yy}-{mm}-{dd}")
    c1 = 0
    c2 = 0
    while c1 == 0:
        y = input("Year: ")
        if y.isdigit() == True:
            c1 = 1
        else:
            print("Invalid value! Please retype.")
    while c2 == 0:
        m = input("Month: ")
        if m.isdigit() == True:
            if int(m) > 0 and int(m) <= 12:
                c2 = 1
            else:
                print("Invalid value! Please retype.")
        else:
            print("Invalid value! Please retype.")
    print(calendar.month(int(y), int(m)))

registerCmd().register("calendar", "Show a calendar", "Tools", calendar)