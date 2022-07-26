from scipy import integrate

N0=0
S0=0
I0=0
R0=0
t=0

def SIR_model_t(SIR,t,beta,gamma):
    global N0
    ''' Simple SIR model
        S: susceptible population
        t: time step, mandatory for integral.odeint
        I: infected people
        R: recovered people
        beta: 
        
        overall condition is that the sum of changes (differnces) sum up to 0
        dS+dI+dR=0
        S+I+R= N (constant size of population)
    
    '''
    
    S,I,R=SIR
    dS_dt=-beta*S*I/N0          #S*I is the 
    dI_dt=beta*S*I/N0-gamma*I
    dR_dt=gamma*I
    return dS_dt,dI_dt,dR_dt

def fit_odeint(x, beta, gamma):
    '''
    helper function for the integration.
    Modification made: fit the summed cases N0-S instead of the active cases I as the provided/compared data is also the summed up total case number.
    '''
    global S0, I0, R0, t
    return N0 - integrate.odeint(SIR_model_t, (S0, I0, R0), t, args=(beta, gamma))[:,0]    # return total summed cases (=N0-S)