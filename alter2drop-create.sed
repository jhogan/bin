# Change ALTER PROC statements to 
# DROP-and-CREATE statements.
s/^\(ALTER\|CREATE\)[ |\t]\+\(PROC\|PROCEDURE\)[ |\t]\(.\+\)/\
IF OBJECT_ID('\3') IS NOT NULL \
BEGIN \
        PRINT N'-Dropping proc \3' \
        DROP PROC \3 \
        IF @@ERROR<>0 AND @@TRANCOUNT>0 ROLLBACK TRANSACTION \
        IF @@TRANCOUNT=0 BEGIN INSERT INTO #tmpErrors (Error) SELECT 1 BEGIN TRANSACTION END \
END \
PRINT N'-Creating proc \3' \
GO\
CREATE \2 \3/i
