
echo -e "\t============================================\n\tGenerated $(date '+%F %T\t%Z %z')\n\t============================================\n\n" > \
    CHANGELOG.md & git log --all --date=relative --pretty=format:"%x09 %h %ad %d %s (%aN)" | grep -v "Merge pull" >> CHANGELOG.md
