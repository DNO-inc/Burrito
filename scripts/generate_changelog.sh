
echo -e "\n\tGenerated $(date '+%F %T')\n\n" > CHANGELOG.md & git log --all --date=relative --pretty=format:"%h %x09 %ad %d %s (%aN)" >> CHANGELOG.md
