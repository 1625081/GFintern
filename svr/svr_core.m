function [A,B] = svr_core(xlsx_addr,ans_addr)
    share_num = 4;
    %xlsx_addr = 'C:\Users\sanjin\OneDrive\Documents\WeChat Files\wxid_nr7znnd3r8c511\FileStorage\File\2021-06\MAPR数值实验\NewRate.xlsx';
    %ans_addr = 'C:\Users\sanjin\OneDrive\Documents\WeChat Files\wxid_nr7znnd3r8c511\FileStorage\File\2021-06\MAPR数值实验\FundInterest.xlsx';
    List = ["601012.SH","300750.SZ","600900.SH","002812.SZ"];
    opts = detectImportOptions(xlsx_addr);
    I_M = cell(1,share_num);
    for i=1:share_num
        %opts.Sheet = List(i);
        %opts.DataRange = 'D1:D138'; 
        %opts.DataRange = '2:11';
        I = readmatrix(xlsx_addr,'Sheet',List(i),'Range','D1:D138');
        % 归一化处理
        I = (I-min(I))/(max(I)-min(I));
        I_M{i} = I;
    end
    opts = detectImportOptions(ans_addr);
    ANS = readmatrix(ans_addr,'Sheet','1','Range','D1:D138');
    % 归一化处理
    ANS = (ANS-min(ANS))/(max(ANS)-min(ANS));
    epsilon = .001;
    C = 100;
    %% 窗口期
    n = 8;
    train_max = 100;
    train_num = 20;
    x = cell(train_num,2);
    test_num = 30;
    y = cell(test_num,2);
    %% 随机选择训练数据、构建测试集数据
    train_set = ceil(linspace(1,train_max,train_num));
    test_set = (101:101+test_num-1);
    m = [.315,.313,.242,.129]; % 配比权重
    Y_train=[];
    Y_test=[];
    for i=1:train_num
        start = train_set(i);
        x{i,1} =  zeros(share_num,n);
        for j=1:share_num
           sheet = I_M{j};
           data = sheet(start:start+n-1)';
           x{i,1}(j,:) = data;
        end
        x{i,2} = ANS(start+n);
        Y_train = [Y_train;ANS(start+n)];
    end
    for i=1:test_num
        start = test_set(i);
        y{i,1} =  zeros(share_num,n);
        for j=1:share_num
           sheet = I_M{j};
           data = sheet(start:start+n-1)';
           y{i,1}(j,:) = data;
        end
        y{i,2} = ANS(start+n);
        Y_test = [Y_test;ANS(start+n)];
    end
    %% 算法开始
    % kernel function
    gamma = .1;
    A=zeros(1,n);B=zeros(1,n);
    K = @(A,B) exp(-gamma*(A-B)*(A-B)');
    M = m'*m;
    %phi M phi'
    pMp = zeros(train_num,train_num);
    for i=1:train_num
        for j=1:train_num
            s = 0;
            tempX = x{i,1};
            tempY = x{j,1};
            for k1=1:share_num
                for k2=1:share_num
                    s = s + K(tempX(k1,:),tempY(k2,:))*M(k1,k2);
                end
            end
            pMp(i,j) = s;
        end
    end
    cvx_begin
        variables alpha_star(train_num) alpha_n(train_num)
        maximize(-0.5*quad_form(alpha_star-alpha_n,pMp)+Y_train'*alpha_star-Y_train'*alpha_n-epsilon*sum(alpha_star)-epsilon*sum(alpha_n))
        subject to
            alpha_n <= C
            alpha_n >= 0
            alpha_star <= C
            alpha_star >= 0
            sum( alpha_star-alpha_n ) == 0
    cvx_end
    %% Test phase
    % 解向量的构建
    predict = zeros(test_num,1);
    ansY = zeros(test_num,1);
    for l=1:test_num
        tempY = y{l,1};
        solve_vec = zeros(train_num,1);
        for i=1:train_num
            tempS = 0;
            tempX = x{i,1};
            for j=1:share_num
                for k=1:share_num
                    tempS = tempS + m(j)*m(k)*K(tempX(j,:),tempY(k,:));
                end
            end
            solve_vec(i) = tempS;
        end
        predict(l) = (alpha_star-alpha_n)'*solve_vec;
        ansY(l) = y{l,2};
    end
    A = mse(predict-ansY);
    B = mae(predict-ansY);
end