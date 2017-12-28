function [T,p] = cholcov_eigs(Sigma,flag)
%CHOLCOV  Cholesky-like decomposition for covariance matrix.
%   T = CHOLCOV(SIGMA) computes T such that SIGMA = T'*T.  SIGMA must be
%   square, symmetric, and positive semi-definite.  If SIGMA is positive
%   definite, then T is the square, upper triangular Cholesky factor.
%
%   If SIGMA is not positive definite, T is computed from an eigenvalue
%   decomposition of SIGMA.  T is not necessarily triangular or square in
%   this case.  Any eigenvectors whose corresponding eigenvalue is close to
%   zero (within a small tolerance) are omitted.  If any remaining
%   eigenvalues are negative, T is empty.
%
%   [T,P] = CHOLCOV(SIGMA) returns the number of negative eigenvalues of
%   SIGMA, and T is empty if P>0.  If P==0, SIGMA is positive semi-definite.
%
%   If SIGMA is not square and symmetric, P is NaN and T is empty.
%
%   [T,P] = CHOLCOV(SIGMA,0) returns P==0 if SIGMA is positive definite, and
%   T is the Cholesky factor.  If SIGMA is not positive definite, P is a
%   positive integer and T is empty.  [...] = CHOLCOV(SIGMA,1) is equivalent
%   to [...] = CHOLCOV(SIGMA).
%
%   Example:
%   Factor a rank-deficient covariance matrix C.
%       C = [2 1 1 2;1 2 1 2;1 1 2 2;2 2 2 3]
%       T = cholcov(C)
%       C2 = T'*T
%   Generate data with this covariance (aside from random variation).
%       C3 = cov(randn(10000,3)*T)
%
%   See also CHOL.

%   Copyright 1993-2015 The MathWorks, Inc.


if nargin < 2, flag = 1; end

% Test for square, symmetric
[n,m] = size(Sigma);
wassparse = issparse(Sigma);
tol = 10*eps(max(abs(diag(Sigma))));
if (n == m) && all(all(abs(Sigma - Sigma') < tol))
    [T,p] = chol(Sigma);

    if p > 0
        % Test for positive definiteness
        if flag
            % Can get factors of the form Sigma==T'*T using the eigenvalue
            % decomposition of a symmetric matrix, so long as the matrix
            % is positive semi-definite.
            [U,D] = eigs(full((Sigma+Sigma')/2),100);

            % Pick eigenvector direction so max abs coordinate is positive
            [~,maxind] = max(abs(U),[],1);
            disp('size U')
            size(U)
            negloc = (U(maxind + (0:n:(100-1)*n)) < 0);
            U(:,negloc) = -U(:,negloc);

            D = diag(D);
            tol = eps(max(D)) * length(D);
            t = (abs(D) > tol);
            D = D(t);
            p = sum(D<0); % number of negative eigenvalues

            if (p==0)
                T = diag(sqrt(D)) * U(:,t)';
            else
                T = zeros(0,'like',Sigma);
            end
        else
            T = zeros(0,'like',Sigma);
        end
    end

else
    T = zeros(0,'like',Sigma);
    p = nan('like',Sigma);
end

if wassparse
    T = sparse(T);
end
