% New version of decomposition.
% jem, 2008-05-04.

cvx_clear(); cvx_quiet(true);

% Number of subsystems.
K = 5;

% Describe nets in an intuitive way.
N = 4; cs = cell(N, 1); cs{1} = [1 2 4]; cs{2} = [2 5]; cs{3} = [3 4]; cs{4} = [4 5];

% Construct the netlist using the given edges.
Es = cell(K, 1); E = []; ps = [];
for k = 1:K
	Es{k} = zeros(0, N);
	for i = 1:N
		if any(cs{i} == k)
			Es{k} = [Es{k}; zeros(1, N)];
			Es{k}(end, i) = 1;
		end
	end
	ps = [ps; size(Es{k}, 1)];
	E = [E; Es{k}];
end
p = sum(ps); % number of public variables (number of copies of net variables).

% Solve centralized problem using CVX.
cvx_begin
	% Define the N net variables only.
	variable z(N);

	% Construct objective function.
	o = 0;
	for i = 1:K
		o = o + phi(i, Es{i}*z);
	end
	minimize(o);
cvx_end
f_opt = cvx_optval;

% Distributed method using dual decomposition.
MAX_ITER = 12; alpha = 0.5; % fixed step size.

nu = zeros(p, 1); % initial dual point.
flower = []; fupper = []; bupper = []; residual = [];

for iter = 1:MAX_ITER
	disp(iter);
	y = zeros(p, 1);
	q = zeros(K, 1);
	for i = 1:K
		nu_i = nu(1 + sum(ps(1:i-1)):sum(ps(1:i)));
		cvx_begin
			variable y_i(ps(i));
			minimize(phi(i, y_i) + nu_i'*y_i);
		cvx_end
		y(1 + sum(ps(1:i-1)):sum(ps(1:i))) = y_i;
		q(i) = cvx_optval;
	end

	% Compute average value of public variables over each net.
	zhat = E\y;
	yhat = E*zhat;

	% Update prices on public variables.
	nu = nu + alpha*(y - E*zhat);

	% Lower bound on objective.
	flower = [flower; sum(q)];

	% Consistency constraint residual.
	residual = [residual; norm(y - E*zhat)];

	% Compute better upper bound by re-solving primal problems with zhat.
	o = 0;
	for i = 1:K
		y_i = yhat(1 + sum(ps(1:i-1)):sum(ps(1:i)));
		o = o + phi(i, y_i);
	end
	fupper = [fupper; o];
end

iters = 1:12;
figure(1); clf; hold on;
set(gca, 'FontSize', 18);
plot(iters, flower(iters), 'b-', 'LineWidth', 1.5)
plot(iters, fupper(iters), 'k--', 'LineWidth', 1.5)
xlabel('k');
legend('flower b', 'fupper b');
%print -depsc2 pwl_quadratic_bounds

figure(2); clf;
set(gca, 'FontSize', 18);
semilogy(iters, residual(iters), 'LineWidth', 1.5);
xlabel('k'); ylabel('residual');
%print -depsc2 pwl_quadratic_residual
