cd /tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad
for t in ${@:-tme t4 tnotes tcare tinter tdeck tsky texplore tlore ttaint tms tau tsrs ttitan tlynx tstrider twindkoi tmnemo tcabbfrog tskywhale tsix tend treq tgarden tgar2 tobs tobs2 tobs3}; do echo "== $t"; timeout 600 python3 $t.py $( [ $t = tsix ] && echo $PWD || echo t4shot) > out_$t.txt 2>&1; grep -E "FAIL|Error:|Traceback" out_$t.txt | head -8; echo "pass $(grep -c '^PASS' out_$t.txt)"; done
echo ALLDONE
