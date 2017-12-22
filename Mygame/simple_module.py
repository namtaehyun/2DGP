def add(a,b):
    return a+b

def main():
    print("This Program is Adder Library")

if __name__ =='__main__':
   main()





#__name__은 단독으로 실행될경우 __main__이된다
#하지만 다른 모듈에서 불러서 실행할경우 simple_module이 된다.
#혼자 사용되는지, 다른모듈에서 불려서 실행되는지를 알수 있다.