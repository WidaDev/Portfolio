# UTF_8
# Python3.11.1, by Timothé, 12/06/2023
import datetime
import time

clock_base = time.time()


class PasswordGenerator:
    def __init__(self,lenPassword):
        self.password = ""
        self.size = lenPassword

        int: self.microSecond = 0
        int: self.hour = 0
        int: self.second = 0
        int: self.minute = 0
        int: self.product = 0

        int: self.seed = 0
        int: self.lastFour = 0
        int: self.type = 0

        int: self.code = 0

    def get_time(self):
        self.microSecond = datetime.datetime.now().microsecond + 1
        self.hour = datetime.datetime.now().hour + 1
        self.second = datetime.datetime.now().second + 1
        self.minute = datetime.datetime.now().minute + 1

    def seed_generation(self):
        self.get_time()
        self.product = self.hour * self.minute * self.second
        self.seed = str(self.product/self.microSecond).split('.')[1]
  
        self.three_last()
       
    def character_choose(self):
        self.lastFour = int(self.seed) % 10000
        self.type = self.lastFour % 4  
        match self.type:
            case 0:
                self.special()
            case 1:
                self.num()
            case 2:
                self.min()
            case 3:
                self.maj()
                
        self.three_last()
    
    def special(self):
        if int(self.seed) % 3 == 0:
            self.password += chr((int(self.code) % 15)+33)
        elif int(self.seed) % 3 == 1:
            self.password += chr((int(self.code) % 7)+58)
        else:
            self.password += chr(126)
        
    def num(self):
        self.password += chr((int(self.code) % 10)+48)
        
    def min(self):
        self. password += chr((int(self.code) % 26)+97)
        
    def maj(self):
        self.password += chr((int(self.code) % 26)+65)
    
    def three_last(self):
        if len(str(self.seed)) >= 3 and len(str(self.password)) < self.size:
            try:
                self.code = int(self.seed) % 1000
                self.seed = round(int(self.seed)/1000)
                self.character_choose()
            except ValueError:
                time.sleep(0.05)
                self.seed_generation()
            
        elif len(str(self.password)) >= self.size:
            print("Le mot de passe est :", self.password)
            print(f"Temps d'éxécution : {round(time.time()-clock_base, 4)} secondes.")
            pass
        
        elif len(str(self.seed)) < 3:
            time.sleep(0.1)
            self.seed_generation()


def main():
    password = PasswordGenerator(lenPassword=10)
    password.seed_generation()


if __name__ == '__main__':
    main()
