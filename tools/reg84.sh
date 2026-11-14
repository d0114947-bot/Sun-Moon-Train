cd /tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad
for t in tact3 tact2 tpre2 tact1; do echo "== $t"; timeout 1200 python3 $t.py > out_$t.txt 2>&1; tail -1 out_$t.txt; grep FAIL out_$t.txt|head; done
echo "== pix"; timeout 600 python3 pix.py check 2>&1 | tail -2
bash runall.sh
for t in tearly tcrisis tbank tlife tevo tworld tbye tforage tsave66 tv77; do echo "== $t"; timeout 900 python3 $t.py > out_$t.txt 2>&1; tail -1 out_$t.txt; grep FAIL out_$t.txt|head -5; done
echo REGDONE
