import numpy as np
import scipy.sparse as spar
import scipy.linalg as la
from scipy.sparse import linalg as sla

def adj_mat(datafile, n):
    """ Parse the data stored in 'datafile' and form the
    adjacency matrix of the corresponding graph.
    'n' is the number of rows of the nxn sparse matrix formed. """
    adj = spar.dok_matrix((n,n))
    with open(datafile, 'r') as f:
        for L in f:
            L = L.strip().split()
            try:
                x, y = int(L[0]), int(L[1])
                adj[x, y] = 1
            except:
                continue
    return adj


def page_rank_dense_lstsq(datafile, d, datasize, n=None):
    """ Solve the page rank problem, given the data in 'datafile',
    the dampening factor 'd', the size 'datasize' of the dataset,
    and the number 'n' of nodes to include.
    Have 'n' default to None.
    Use the method involving least squares."""
    data = adj_mat(datafile, n)
    A = np.asarray(data.tocsr()[:n, :n].todense())
    #data is dense and is of type matrix
    e = np.ones(n)
    for i, v in enumerate(A.sum(1)):
        if v == 0:
            A[i] = e
    
    K = ((1./A.sum(1))[:,np.newaxis]*A).T
    K *= - d
    np.fill_diagonal(K, K.diagonal() + 1)
    R = la.lstsq(K, (1-d)*e/float(n))
    max_rank = R[0].max()
    
    return max_rank, np.where(R[0]==max_rank)[0]

def page_rank_dense_iter(datafile, d, datasize, n=None, tol=1E-5):
    """ Solve the page rank problem, given the data in 'datafile',
    the dampening factor 'd', the size 'datasize' of the dataset,
    the number 'n' of nodes to include, and a tolerance 'tol'
    to use to determine when to stop iterating.
    Have 'n' default to None.
    Use the iterative method described in the lab. """
    pass

def page_rank_dense_eig(datafile, d, datasize, n=None):
    """ Solve the page rank problem, given the data in 'datafile',
    the dampening factor 'd', the size 'datasize' of the dataset,
    and the number 'n' of nodes to include.
    Have 'n' default to None.
    Use the eigenvalue method described in the lab. """
    pass
  
def sparse_pr(datafile, d, datasize, n=None, tol=1e-5):
    """ Solve the page rank problem, given the data in 'datafile',
    the dampening factor 'd', the size 'datasize' of the dataset,
    the number 'n' of nodes to include, and a tolerance 'tol'
    to use to determine when to stop iterating.
    Have 'n' default to None.
    Use the iterative method described in the lab.
    Use only sparse matrix operations. """
    
    A = data.tocsc()[:n, :n]
    s = A.sum(1)
    diag = 1./s
    sinks = s==0
    diag[sinks] = 0
    K = spar.spdiags(diag.squeeze(1), 0, n, n).dot(A).T
    
    d = .85
    convDist = 1
    Rinit = np.ones((n, 1))/float(n)
    Rold = Rinit
    while convDist > tol:
        Rnew = d*K.dot(Rold) + (1-d)*Rinit + (d*Rold[sinks].sum())*Rinit
        convDist = la.norm(Rnew-Rold)
        Rold = Rnew
        
    max_rank = Rnew.max()
    return max_rank, Rnew[Rnew==max_rank]
