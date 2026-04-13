%% Parâmetros do circuito
R   = 1000;     % Resistência [Ohm]
C   = 100e-6;   % Capacitância [F]
V0  = 5;        % Tensão da fonte [V]
tau = R * C;    % Constante de tempo [s]

%% Parâmetros da simulação
t_sim = 5 * tau;    % Simular por 5 constantes de tempo
t_step = tau / 100; % Passo de tempo (100 pontos por tau)

fprintf('=== Parâmetros do Circuito RC ===\n')
fprintf('R   = %.0f Ohm\n', R)
fprintf('C   = %.0f uF\n', C * 1e6)
fprintf('tau = %.4f s\n', tau)
fprintf('V0  = %.1f V\n', V0)
fprintf('Simulando ate t = %.3f s\n', t_sim)

%% Exportar para planilha
time    = tout; 
voltage = voltage(:,1);
current = current(:,1); 

T = table(time, voltage, current, ...
    'VariableNames', {'time_s', 'voltage_V', 'current_A'});

writetable(T, '../data/simulation_output.csv');
fprintf('Dados exportados para data/simulation_output.csv\n');
fprintf('Total de amostras: %d\n', height(T));