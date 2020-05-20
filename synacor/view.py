# pylint: disable = attribute-defined-outside-init

from binaryninja import (
    Architecture, BinaryView, SectionSemantics, SegmentFlag as Flag
)

class SynacorView(BinaryView):
    name = 'Synacor'
    long_name = 'Synacor Program'

    @classmethod
    def is_valid_for_data(cls, data):
        # No reliable way to determine whether given data is a legit Synacor
        # program, so rely on extension .synbin instead
        return data.file.original_filename.endswith('.synbin')

    def __init__(self, data):
        BinaryView.__init__(self, parent_view=data, file_metadata=data.file)
        self.raw = data

    def init(self):
        self.arch = Architecture['Synacor']
        self.platform = Architecture['Synacor'].standalone_platform

        self.add_auto_segment(
            0, len(self.raw), # entire program is self-modifiable
            0, len(self.raw),
            Flag.SegmentReadable | Flag.SegmentExecutable | Flag.SegmentWritable
        )

        # TODO: Is this correct?
        self.add_user_section(
            'synacor', 0, len(self.raw),
            SectionSemantics.ReadOnlyCodeSectionSemantics
        )

        self.add_entry_point(0)
        return True

    def perform_is_executable(self):
        return True
