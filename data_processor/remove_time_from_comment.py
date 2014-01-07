import codecs

commentDataFile = codecs.open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/commentData.csv", "r", encoding="utf-8")
preProcessedCommentDataFile = codecs.open("/Users/jeremy/Google Drive/PSU/thesis/itunes_data/preProcessedCommentData.csv", "w")

# header
commentDataHeader = commentDataFile.readline()[:-1]


def remove_time(date_attribute):
    """
    The raw date is in "MM/DD/yyyy HH:mm:ss AM" format. Only keeps MM/DD/yyyy part.
    """
    return date_attribute[1:-1].split(" ")[0]

preProcessedCommentDataFile.write(commentDataHeader)

for line in commentDataFile:
    fields = line.split(",")
    date_str = "\"" + remove_time(fields[2]) + "\""
    fields[2] = date_str
    new_line = fields[0] + "," + fields[1] + "," + fields[2] + "," + fields[3]
    preProcessedCommentDataFile.write(new_line)

commentDataFile.close()
preProcessedCommentDataFile.close()