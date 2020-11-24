DELETE
FROM "Message"
WHERE "Dep_Id" NOT IN( SELECT "Dep_Id"
                       FROM "Department"
                       WHERE "Actual" IS NOT NULL )