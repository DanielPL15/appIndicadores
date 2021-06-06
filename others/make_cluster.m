function [indices_cluster1,centroides,paises_clusters] = make_cluster(variables,etiquetas_paises,num_clusters,tipo_cluster)
%{
Salida: Indices_cluster1: Vector que contiene numeros correspondientes a los clusters asignados a cada variable
                          Las variables no asignadas ningún clsuter se dejan con valor 0 
        Centroides de los clusters
        Paises de los clusters lista de paiese de cada cluster
Entrada: variables: matriz con columnas correspondientes a las variables (puede tener NaN)
                    num_cluster: numero de clusters a realizar
         tipo_cluster: tipo de cluster 1 - Kmeans
                                       2 - dendrograma
                                       3 - redes neuronales
%}


x = variables;

%Elimina las filas que tienen al gún dato en blanco
t1 = table(x, etiquetas_paises);
t2 = rmmissing(t1);
etiquetas_filtradas = table2cell(t2(1:end,2));
x1 = rmmissing(x);
x2 = transpose(x1);
x = x2;


if (tipo_cluster==3)
    n_neuronas_x =1;
    n_neuronas_y =num_clusters;
    net = selforgmap([n_neuronas_x  n_neuronas_y]);
    net.trainParam.epochs = 5000; %número de entrenamientos
    net.trainParam.showWindow = false; %deshabilita la ventana de salida
    [net,tr] = train(net,x);

    %nntraintool
    %calcula la clase para cada una de las entradas y la almacena en 
    % y poniendoe un 1 en la clase y cero en el resto resto
    y = net(x);  
    % pasa a numero la clase
    classes = vec2ind(y);    %numero de cluster para cada pais
    centroides=NaN(1,1);
end
if (tipo_cluster==1)
%     [classes2, C] = kmeans(x',num_clusters); %clacula clusters por k-means
     [classes2, C] = kmeans(x',num_clusters,'Start','uniform','Replicates',5); %clacula clusters por k-means
    
    classes = classes2'; %K-means en lugar de redes neuronales
    centroides = C;
elseif (tipo_cluster==2)
    % dendrogramas
    X=x';
    Z = linkage(X,'ward');
    %Z = linkage(X,'single');
    T = cluster(Z,'maxclust',num_clusters);
    %fig = dendrogram(Z);
    %dendrogram(Z,200,'ColorThreshold',cutoff,'Orientation','left','Labels',etiquetas_filtradas );
    classes = T';
    centroides=NaN(1,1);
end
[n, n_paises] = size(classes);
%neurona = zeros(n_neuronas_x*n_neuronas_y,1);
clear nn;
clear neurona;
%nn(1:n_neuronas_x*n_neuronas_y)=0;

nn(1:num_clusters)=0;
for n_pas=1:n_paises
    nn(classes(n_pas))= nn(classes(n_pas))+1;
    neurona(classes(n_pas),nn(classes(n_pas))) = etiquetas_filtradas(n_pas);
end
indices_cluster=classes';
paises_clusters=neurona';

%calcula vector original de países

[n1, ~] = size(etiquetas_paises);
[n2, ~]  = size(indices_cluster);
indices_cluster1 = zeros(n1,1);
for i1=1:n1
    for i2=1:n2
        if(strcmp(etiquetas_paises(i1),etiquetas_filtradas(i2)))
            indices_cluster1(i1)=indices_cluster(i2); 
            break;
        end
    end
end

end       
       

%{
for i=1:n_neuronas_x*n_neuronas_y
 %   i
  %  neurona(i,:)
%end
 n_cluster = linspace(1,n_neuronas_x*n_neuronas_y,n_neuronas_x*n_neuronas_y);
 
 borra = NaN(200);
 writematrix(borra,'out_NN1.xlsx','Sheet',1,'Range','A1')
 writematrix(nn,'out_NN1.xlsx','Sheet',1,'Range','C1')
 writematrix(n_cluster,'out_NN1.xlsx','Sheet',1,'Range','C2')
 writecell(neurona','out_NN1.xlsx','Sheet',1,'Range','C3')
 
 writematrix(borra,'out_NN1.xlsx','Sheet',2,'Range','B2')
 writematrix(classes','out_NN1.xlsx','Sheet',2,'Range','C3') 
 writecell(etiquetas_filtradas,'out_NN1.xlsx','Sheet',2,'Range','B3')
 clear borra;
 
 %}


 
