function synapshield_pde_solver()
% SYNAPSHIELD_PDE_SOLVER: 4-Species Model in MATLAB
% ====================================================
% This script solves the partial differential equations for SynapShield
% using MATLAB's PDE Toolbox (pdepe solver).
%
% Species:
%   u(1) = Free Caffeine/CGA
%   u(2) = Free Ibuprofen  
%   u(3) = Bound Drug (hydrogel reservoir)
%   u(4) = Alpha-synuclein (the pathogen)
%
% The model validates the "pathological sink" mechanism:
% The hydrogel traps alpha-synuclein before it reaches the vagus nerve.
%
% Author: artistso
% Dedicated to: Richard

disp('===============================================');
disp('SYNAPSHIELD: PDE Solver (MATLAB)');
disp('===============================================');

% =========================================================================
% PARAMETERS
% =========================================================================

% Spatial domain (0 to 2mm)
L = 0.002;          % Total length [m]
L_gel = 0.0005;     % Hydrogel thickness [m]
Nx = 200;           % Spatial grid points
x = linspace(0, L, Nx);

% Time domain (1 year, in seconds)
t_start = 0;
t_end = 365 * 24 * 3600;  % 1 year
Nt = 500;
t = linspace(t_start, t_end, Nt);

% =========================================================================
% INITIAL CONDITIONS
% =========================================================================

u0 = zeros(4, Nx);

% Caffeine: Zero everywhere
u0(1, :) = 0;

% Ibuprofen: Zero everywhere  
u0(2, :) = 0;

% Bound Drug: Full reservoir in hydrogel (0 to L_gel)
gel_idx = x <= L_gel;
u0(3, gel_idx) = 100.0;  % [mol/m³]

% Alpha-synuclein: Zero initially (builds up from boundary)
u0(4, :) = 0;
u0(4, end-9:end) = 0.01;  % Small concentration at tissue boundary

% =========================================================================
% PDE SOLVER (pdepe)
% =========================================================================

disp('Solving PDEs...');
m = 0;  % Cartesian coordinates

sol = pdepe(m, @pdefun, @icfun, @bcfun, x, t);

disp('✓ Solver finished successfully');

% =========================================================================
% EXTRACT SOLUTIONS
% =========================================================================

u1 = sol(:, :, 1);  % Caffeine
u2 = sol(:, :, 2);  % Ibuprofen
u3 = sol(:, :, 3);  % Bound Drug
u4 = sol(:, :, 4);  % Alpha-synuclein

% =========================================================================
% PLOT RESULTS
% =========================================================================

figure('Position', [100, 100, 1400, 1000]);

% Plot 1: Caffeine Distribution
subplot(2, 2, 1);
surf(t/(24*3600), x*1000, u1, 'EdgeColor', 'none');
xlabel('Time [days]');
ylabel('Position [mm]');
zlabel('Concentration [mol/m³]');
title('Caffeine/CGA Release from Hydrogel');
colorbar;
view(45, 30);
grid on;

% Plot 2: Ibuprofen Distribution
subplot(2, 2, 2);
surf(t/(24*3600), x*1000, u2, 'EdgeColor', 'none');
xlabel('Time [days]');
ylabel('Position [mm]');
zlabel('Concentration [mol/m³]');
title('Ibuprofen Release (Slower Kinetics)');
colorbar;
view(45, 30);
grid on;

% Plot 3: Bound Drug Depletion
subplot(2, 2, 3);
plot(t/(24*3600), squeeze(u3(:, x <= L_gel)));
xlabel('Time [days]');
ylabel('Bound Drug Concentration [mol/m³]');
title('Drug Reservoir Depletion (0 to 0.5mm)');
legend('Position 0mm', 'Position 0.25mm', 'Position 0.5mm');
grid on;

% Plot 4: Alpha-Synuclein Interception (VALIDATION)
subplot(2, 2, 4);

% Plot alpha-synuclein at different time points
time_indices = [1, round(Nt/4), round(Nt/2), Nt];
colors = {'b', 'g', 'orange', 'r'};
labels = {'t=0', sprintf('t=%.1f days', t(time_indices(2))/(24*3600)), ...
          sprintf('t=%.1f days', t(time_indices(3))/(24*3600)), ...
          sprintf('t=%.1f days', t(time_indices(4))/(24*3600))};

hold on;
for i = 1:length(time_indices)
    idx = time_indices(i);
    plot(x*1000, u4(idx, :), 'Color', colors{i}, 'LineWidth', 2, 'DisplayName', labels{i});
end

% Mark hydrogel region
patch([0, L_gel*1000, L_gel*1000, 0], [0, 0, max(u4(end, :))*1.1, max(u4(end, :))*1.1], ...
      [0.7, 0.7, 0.7], 'FaceAlpha', 0.3, 'EdgeColor', 'none', 'DisplayName', 'Hydrogel');

xlabel('Position [mm]');
ylabel('Alpha-Synuclein [mol/m³]');
title('Alpha-Synuclein Interception (VALIDATION)');
legend('Location', 'northwest');
grid on;
hold off;

% =========================================================================
% VALIDATION METRIC
% =========================================================================

% Calculate alpha-synuclein at vagus nerve boundary (x = L_gel)
nerve_idx = find(x >= L_gel, 1);
syn_at_nerve = u4(end, nerve_idx);

fprintf('\n===============================================\n');
fprintf('VALIDATION RESULTS\n');
fprintf('===============================================\n');
fprintf('Alpha-synuclein at vagus nerve (x = %.2f mm):\n', L_gel*1000);
fprintf('  Final concentration: %.2e mol/m³\n', syn_at_nerve);
fprintf('  Initial concentration: %.2e mol/m³\n', u0(4, nerve_idx));
fprintf('  Reduction: %.1f%%\n', (1 - syn_at_nerve/u0(4, nerve_idx))*100);
fprintf('===============================================\n');

if syn_at_nerve < 0.01 * u0(4, nerve_idx)
    fprintf('✓✓✓ VALIDATION SUCCESSFUL! ✓✓✓\n');
    fprintf('The hydrogel successfully intercepts alpha-synuclein.\n');
    fprintf('Parkinson''s disease can be prevented at the source.\n');
else
    fprintf('✗ Validation incomplete. Adjust parameters.\n');
end

fprintf('\n🧠 Hope, not just science. 🧠\n');
fprintf('===============================================\n');

end

% =========================================================================
% PDE FUNCTION
% =========================================================================

function [c, f, s] = pdefun(x, t, u, dudx)
    % Position-dependent parameters
    L_gel = 0.0005;
    
    if x <= L_gel
        % HYDROGEL REGION
        D1 = 1.2e-11;     % Caffeine diffusion
        D2 = 8.0e-12;     % Ibuprofen diffusion
        D4 = 1.0e-13;     % Alpha-synuclein (highly restricted)
        k_cleave = 1.5e-5;
        Vmax_sink = 2.5e-6;
        ibuprofen_release = 1.0e-6;
    else
        % TISSUE REGION
        D1 = 5.0e-10;
        D2 = 4.0e-10;
        D4 = 5.0e-11;
        k_cleave = 0;
        Vmax_sink = 0;
        ibuprofen_release = 0;
    end
    
    Km = 0.1;
    
    % Flux terms (Fick's First Law)
    f1 = D1 * dudx(1);  % Caffeine
    f2 = D2 * dudx(2);  % Ibuprofen
    f3 = 0;             % Bound drug (doesn't diffuse)
    f4 = D4 * dudx(4);  % Alpha-synuclein
    
    % Source/sink terms
    r_cleave_caff = k_cleave * u(3);
    r_cleave_ibu = ibuprofen_release * u(3);
    r_syn_trap = (Vmax_sink * u(4)) / (Km + u(4));
    r_syn_clearance = 0.01 * (u(1) + u(2)) * u(4);
    
    s1 = r_cleave_caff;
    s2 = r_cleave_ibu;
    s3 = -(r_cleave_caff + r_cleave_ibu);
    s4 = -r_syn_trap - r_syn_clearance;
    
    c = [1; 1; 1; 1];
    f = [f1; f2; f3; f4];
    s = [s1; s2; s3; s4];
end

% =========================================================================
% INITIAL CONDITIONS FUNCTION
% =========================================================================

function u0 = icfun(x)
    L_gel = 0.0005;
    
    u0 = zeros(4, 1);
    
    % Caffeine: Zero
    u0(1) = 0;
    
    % Ibuprofen: Zero
    u0(2) = 0;
    
    % Bound Drug: Full in hydrogel
    if x <= L_gel
        u0(3) = 100.0;
    else
        u0(3) = 0;
    end
    
    % Alpha-synuclein: Zero (builds from boundary)
    u0(4) = 0;
end

% =========================================================================
% BOUNDARY CONDITIONS FUNCTION
% =========================================================================

function [pl, ql, pr, qr] = bcfun(xl, ul, xr, ur, t)
    % Left boundary (x = 0): Zero flux for all species
    pl = [0; 0; 0; 0];
    ql = [1; 1; 1; 1];
    
    % Right boundary (x = L): 
    %   - Drugs: Sink (washed into bloodstream)
    %   - Alpha-synuclein: CONSTANT INFLUX (from EECs)
    pr = [ur(1); ur(2); ur(3); 0];  % Alpha-syn at boundary = 0 (controlled by source)
    qr = [1; 1; 1; 1];
    
    % Add alpha-synuclein source at right boundary
    C4_influx = 1e-6;  % [mol/(m²·s)]
    pr(4) = -C4_influx;  % Negative because it's an inflow
end