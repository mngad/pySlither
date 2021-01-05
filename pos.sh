while read line; do
     X=`echo $line| cut -c1-3`; 
     Y=`echo $line| cut -c4-7`;
     xdotool mousemove --sync $((  0.5 + $X )) $(( 0.5 + $Y ));
     xdotool click 1
done < positions.txt
