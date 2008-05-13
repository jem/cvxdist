function cvx_optval = phi(i, y)

randn('state', i);

K = 5;
m = 20;
n = 10;
ps = [1 2 1 3 2];

A = randn(m, n + ps(i));
b = randn(m, 1);
c = sqrt(2)*randn(n + ps(i), 1);
mu = 0.1;

cvx_begin
	variable x(n);
	w = [x; y];
	minimize(max(A*w + b) + mu*sum_square(w - c));
cvx_end
