node -c <(awk '/<script>/{flag=1; next} /<\/script>/{flag=0} flag' index.html)
node -c <(awk '/<script>/{flag=1; next} /<\/script>/{flag=0} flag' chancla_bomb.html)
