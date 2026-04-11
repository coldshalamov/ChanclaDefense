awk '/<script>/{flag=1; next} /<\/script>/{flag=0} flag' index.html > temp1.js
node -c temp1.js
awk '/<script>/{flag=1; next} /<\/script>/{flag=0} flag' chancla_bomb.html > temp2.js
node -c temp2.js
rm temp1.js temp2.js
