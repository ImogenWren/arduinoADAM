
import time

import time
#print(time.time())

#print(round(time.time()))


class State(object):
    call = 0 # shared state variable
    def next_state(self, cls):
        print('-> %s' % (cls.__name__,)," ")
        self.__class__ = cls

    def show_state(self, i):
        print('%2d:%2d:%s' % (self.call,i,self.__class__.__name__))



class init_state(State):
    __call = 0 # state variable
    def __call__(self,ok):
        # track useage - boilerplate
        self.show_state(self.__call)
        self.call += 1
        self.__call += 1
        #state functions

        #transition
        if ok:
            self.next_state(wait_state)

class wait_state(State):
    __call = 0
    def __call__(self, ok):
        self.show_state(self.__call)
        self.call +=1
        self.__call +=1
        #transition
        if ok:
            self.next_state(do_state)
        else:
            self.next_state(init_state)


class do_state(State):
    __call = 0
    def __call__(self, ok):
        self.show_state(self.__call)
        self.call +=1
        self.__call +=1
        #transition
        if ok:
            self.next_state(init_state)





if __name__ == '__main__':
   sm = init_state()
   for v in [1,1,1,0,0,0,1,1,0,1,1,0,0,1,0,0,1,0,0]:
      sm(v)
   print ('---------')
   print( vars(sm))