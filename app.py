from pyknow import *
import datetime


class Greetings(KnowledgeEngine):
    # Initiate the fact actions, this is the motor behind the knowledge engine
    # If this function is removed no question is asked
    @DefFacts()
    def _initial_action(self):
        yield Fact(action="questions")
        yield Fact(action="advice")
        yield Fact(action="greet")
        yield Fact(month=datetime.datetime.now().month)

    # When someone name is given, say hi
    @Rule(Fact(action='greet'),
          Fact(name=MATCH.name))
    def greet(self, name):
        print("Hi %s!" % (name))

    # Ask for someones name
    @Rule(Fact(action='greet'))
    def ask_name(self):
        self.declare(Fact(name=input("What's your name? ")))

    # Ask fore someones age, and register it as a fact
    @Rule(Fact(action='questions'))
    def ask_age(self):
        self.declare(Fact(age=int(input("What's your age? (ex. 12) "))))

    # Ask for someones temperature and register it as a fact
    @Rule(Fact(action='questions'))
    def ask_temperature(self):
        self.declare(Fact(temp=float(input("What's your temperature? (ex. 37.5) "))))

    # Ask if someone has a headache and register it as a fact
    @Rule(Fact(action='questions'))
    def ask_headache(self):
        self.declare(Fact(headache=bool(int(input("Do you have a headache? (ex. 0) ")))))

    #
    # INFO
    # Information triggers for the user, to give some background information
    #
    @Rule(Fact(month=P(lambda x: x <= 2 or x >= 10)),
          Fact(name=MATCH.name))
    def winter_months(self, name):
        print("\tINFO for %s! High risk of sickness, winter months." % name)
        self.declare(Fact(winter=True))

    @Rule(Fact(age=P(lambda x: x <= 12 or x >= 65)),
        Fact(age=MATCH.age),
        Fact(name=MATCH.name))
    def age_group(self, age, name):
            print("\tINFO for %s! You are %s years old, your age group is more prone to diseases" % (name, age))
            self.declare(Fact(wr_age_group=True))

    @Rule(Fact(temp=P(lambda x: x > 37.0 or x < 35.0)),
          Fact(temp=MATCH.temp),
          Fact(name=MATCH.name))
    def temperature(self, temp, name):
        print("\tINFO for %s! Your body temperature is %s degrees, this is not good" % (name, temp))
        self.declare(Fact(wr_temp=True))

    #
    # ADVICE
    # Advice from the assistant
    #
    @Rule(Fact(action='advice'),
          Fact(headache=True),
          Fact(wr_temp=True))
    def advice_1(self):
        print("ADVICE: A headache with wrong temperature is not good, please consult a doctor")
        self.declare(Fact(advice=True))

    @Rule(Fact(action='advice'),
          Fact(wr_age_group=False),
          Fact(wr_temp=True))
    def advice_2(self):
        print(
            "ADVICE: You are in a good age group, if your temperature does not fall within 2 days, please consult a doctor")
        self.declare(Fact(advice=True))

    @Rule(Fact(action='advice'),
          Fact(winter=True),
          Fact(wr_temp=True))
    def advice_3(self):
        print(
            "ADVICE: In the winter a chance of sickness is higher, don't worry about your wrong temperature")

    @Rule(Fact(action='advice'),
          Fact(winter=True),
          Fact(wr_age_group=True))
    def advice_4(self):
        print(
            "ADVICE: In the winter and in your age group there is a higher chance of sickness, please consult a doctor.")

engine = Greetings()
engine.reset()  # Prepare the engine for the execution.
engine.run()  # Run it!