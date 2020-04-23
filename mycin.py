### Utility functions
def eq(x, y):
    """Function for testing value equality."""
    return x == y

def boolean(string):
    """
    Function for reading True or False from a string.  Raises an error if the
    string is not True or False.
    """
    if string == 'True':
        return True
    if string == 'False':
        return False
    raise ValueError('bool must be True or False')


### Setting up initial data

# Here we define the contexts, parameters, and rules for our system.  This is
# the job of the expert, and in a more polished system, we would define and use
# a domain-specific language to make this easier.

def define_contexts(sh):
    # Patient and symptom have some initial goals--parameters that should be
    # collected before reasoning begins.  This might be useful in some domains;
    # for example, this might be legally required in a medical system.
    sh.define_context(Context('patient', ['name', 'sex', 'age','temp','outside-activity','contact-condition','travel-condition']))
    sh.define_context(Context('symptom', ['vomit-condition', 'cough-condition','diarrhea-condition','breath-condition','days-old']))
    
    # Finding the identity of the virus is our goal.
    sh.define_context(Context('virus', goals=['identity']))

def define_params(sh):
    # Patient params
    sh.define_param(Parameter('name', 'patient', cls=str, ask_first=True))
    sh.define_param(Parameter('sex', 'patient', enum=['M', 'F'], ask_first=True))
    sh.define_param(Parameter('age', 'patient', cls=int, ask_first=True))
    sh.define_param(Parameter('temp', 'patient', enum=['no', 'mild', 'serious'], ask_first=True))
    sh.define_param(Parameter('outside-activity', 'patient', cls=boolean, ask_first=True))
    sh.define_param(Parameter('contact-condition', 'patient', cls=boolean, ask_first=True))
    sh.define_param(Parameter('travel-condition', 'patient', cls=boolean, ask_first=True))
    
    # Symptom params
    sh.define_param(Parameter('vomit-condition', 'symptom', cls=boolean, ask_first=True))
    sh.define_param(Parameter('cough-condition', 'symptom', cls=boolean, ask_first=True))
    sh.define_param(Parameter('diarrhea-condition', 'symptom', cls=boolean, ask_first=True))
    sh.define_param(Parameter('breath-condition', 'symptom', cls=boolean, ask_first=True))

    #sh.define_param(Parameter('site', 'symptom', enum=['blood'], ask_first=True))
    sh.define_param(Parameter('days-old', 'symptom', cls=int, ask_first=True))
    
    # Virus params
    Virus = ['COVID-19', 'Ebola', 'Flu', 'Cold']
    sh.define_param(Parameter('identity', 'virus', enum=Virus, ask_first=True))
    sh.define_param(Parameter('community condition', 'virus', cls=boolean))
    sh.define_param(Parameter('test result', 'virus', enum=['positive', 'negative']))
    
    #sh.define_param(Parameter('aerobicity', 'virus', enum=['aerobic', 'anaerobic']))
    #sh.define_param(Parameter('growth-conformation', 'virus',
    #                          enum=['chains', 'pairs', 'clumps']))

def define_rules(sh):
    sh.define_rule(Rule(52,
                        [('temp', 'patient', eq, 'serious'),
                         ('outside-activity', 'patient', eq, True),
                         ('travel-activity','patient', eq, True),
                         ('vomit-condition', 'symptom', eq, True),
                         ('cough condition','symptom', eq, True),
                         ('diarrhea-condition','symptom', eq, True),
                         ('breath condition','symptom', eq, True)],
                        [('identity', 'virus', eq, 'COVID-19')],
                        0.7))
    sh.define_rule(Rule(71,
                        [('gram', 'virus', eq, 'pos'),
                         ('morphology', 'virus', eq, 'coccus'),
                         ('growth-conformation', 'virus', eq, 'clumps')],
                        [('identity', 'virus', eq, 'staphylococcus')],
                        0.7))
    sh.define_rule(Rule(73,
                        [('site', 'symptom', eq, 'blood'),
                         ('gram', 'virus', eq, 'neg'),
                         ('morphology', 'virus', eq, 'rod'),
                         ('aerobicity', 'virus', eq, 'anaerobic')],
                        [('identity', 'virus', eq, 'bacteroides')],
                        0.9))
    sh.define_rule(Rule(75,
                        [('gram', 'virus', eq, 'neg'),
                         ('morphology', 'virus', eq, 'rod'),
                         ('compromised-host', 'patient', eq, True)],
                        [('identity', 'virus', eq, 'pseudomonas')],
                        0.6))
    sh.define_rule(Rule(107,
                        [('gram', 'virus', eq, 'neg'),
                         ('morphology', 'virus', eq, 'rod'),
                         ('aerobicity', 'virus', eq, 'aerobic')],
                        [('identity', 'virus', eq, 'enterobacteriaceae')],
                        0.8))
    sh.define_rule(Rule(165,
                        [('gram', 'virus', eq, 'pos'),
                         ('morphology', 'virus', eq, 'coccus'),
                         ('growth-conformation', 'virus', eq, 'chains')],
                        [('identity', 'virus', eq, 'streptococcus')],
                        0.7))


### Running the system

import logging
from emycin import Parameter, Context, Rule, Shell

def report_findings(findings):
    for inst, result in findings.items():
        print('Findings for %s-%d:' % (inst[0], inst[1]))
        for param, vals in result.items():
            possibilities = ['%s: %f' % (val[0], val[1]) for val in vals.items()]
            print('%s: %s' % (param, ', '.join(possibilities)))
        
#def main():
sh = Shell()
define_contexts(sh)
define_params(sh)
define_rules(sh)
report_findings(sh.execute(['patient', 'symptom', 'virus']))
