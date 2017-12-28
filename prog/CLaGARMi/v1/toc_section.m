%stores string and toc value in cell array to keep track of section timings

function st=toc_section(st,sec_name)

n_sec=size(st,1)+1;
st{n_sec,1}=sec_name;
st{n_sec,3}=toc;
if n_sec<=1
    st{n_sec,2}=toc;
else
    st{n_sec,2}=toc-st{n_sec-1,3};
end

disp([sec_name ':  ' num2str(st{n_sec,2},2) ' secs, ' num2str(st{n_sec,2}/60,2) ' mins.' ]);