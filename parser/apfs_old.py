# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum
import struct


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Apfs(KaitaiStruct):

    class ContentType(Enum):
        empty = 0
        history = 9
        location = 11
        files = 14
        extents = 15
        unknown3 = 16

    class EaType(Enum):
        generic = 2
        symlink = 6

    class BlockType(Enum):
        containersuperblock = 1
        rootnode = 2
        node = 3
        spaceman = 5
        allocationinfofile = 7
        btree = 11
        checkpoint = 12
        volumesuperblock = 13
        unknown = 17

    class ItemType(Enum):
        folder = 4
        file = 8
        symlink = 10

    class EntryType(Enum):
        location = 0
        inode = 2
        thread = 3
        extattr = 4
        hardlink = 5
        entry6 = 6
        extent = 8
        name = 9
        entry12 = 12
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self._raw_block0 = self._io.read_bytes(4096)
        io = KaitaiStream(BytesIO(self._raw_block0))
        self.block0 = self._root.Block(io, self, self._root)

    class Volumesuperblock(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.ensure_fixed_contents(struct.pack('4b', 65, 80, 83, 66))
            self.unknown_36 = self._io.read_bytes(92)
            self.block_map_block = self._root.RefBlock(self._io, self, self._root)
            self.root_dir_id = self._io.read_u8le()
            self.inode_map_block = self._root.RefBlock(self._io, self, self._root)
            self.unknown_152_blk = self._root.RefBlock(self._io, self, self._root)
            self.unknown_160 = self._io.read_bytes(80)
            self.volume_guid = self._io.read_bytes(16)
            self.time_updated = self._io.read_u8le()
            self.unknown_264 = self._io.read_u8le()
            self.created_by = (KaitaiStream.bytes_terminate(self._io.read_bytes(32), 0, False)).decode(u"UTF-8")
            self.time_created = self._io.read_u8le()
            self.unknown_312 = self._io.read_bytes(392)
            self.volume_name = (self._io.read_bytes_term(0, False, True, True)).decode(u"UTF-8")


    class ExtentKey(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.offset = self._io.read_u8le()


    class HistoryRecord(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unknown_0 = self._io.read_u4le()
            self.unknown_4 = self._io.read_u4le()


    class LocationKey(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.block_id = self._io.read_u8le()
            self.version = self._io.read_u8le()


    class LocationRecord(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.block_start = self._io.read_u4le()
            self.block_length = self._io.read_u4le()
            self.block_num = self._root.RefBlock(self._io, self, self._root)


    class NodeEntry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.header = self._root.DynamicEntryHeader(self._io, self, self._root)

        @property
        def key(self):
            if hasattr(self, '_m_key'):
                return self._m_key if hasattr(self, '_m_key') else None

            _pos = self._io.pos()
            self._io.seek(((self.header.ofs_key + self._parent.ofs_keys) + 56))
            self._m_key = self._root.Key(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_key if hasattr(self, '_m_key') else None

        @property
        def data(self):
            if hasattr(self, '_m_data'):
                return self._m_data if hasattr(self, '_m_data') else None

            _pos = self._io.pos()
            self._io.seek(((self._root.block_size - self.header.ofs_data) - (40 * (self._parent.type_flags & 1))))
            _on = ((256 if (self._parent.type_flags & 2) == 0 else 0) + (self.key.type_entry.value * (0 if (self._parent.type_flags & 2) == 0 else 1)))
            if _on == self._root.EntryType.entry12.value:
                self._m_data = self._root.T12Record(self._io, self, self._root)
            elif _on == self._root.EntryType.hardlink.value:
                self._m_data = self._root.HardlinkRecord(self._io, self, self._root)
            elif _on == self._root.EntryType.location.value:
                self._m_data = self._root.LocationRecord(self._io, self, self._root)
            elif _on == self._root.EntryType.thread.value:
                self._m_data = self._root.ThreadRecord(self._io, self, self._root)
            elif _on == self._root.EntryType.extent.value:
                self._m_data = self._root.ExtentRecord(self._io, self, self._root)
            elif _on == self._root.EntryType.inode.value:
                self._m_data = self._root.InodeRecord(self._io, self, self._root)
            elif _on == self._root.EntryType.entry6.value:
                self._m_data = self._root.T6Record(self._io, self, self._root)
            elif _on == 256:
                self._m_data = self._root.PointerRecord(self._io, self, self._root)
            elif _on == self._root.EntryType.name.value:
                self._m_data = self._root.NamedRecord(self._io, self, self._root)
            elif _on == self._root.EntryType.extattr.value:
                self._m_data = self._root.ExtattrRecord(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_data if hasattr(self, '_m_data') else None


    class FullEntryHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ofs_key = self._io.read_s2le()
            self.len_key = self._io.read_u2le()
            self.ofs_data = self._io.read_s2le()
            self.len_data = self._io.read_u2le()


    class Allocationinfofile(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unknown_32 = self._io.read_bytes(4)
            self.num_entries = self._io.read_u4le()
            self.entries = [None] * (self.num_entries)
            for i in range(self.num_entries):
                self.entries[i] = self._root.AllocationinfofileEntry(self._io, self, self._root)



    class BlockHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.checksum = self._io.read_u8le()
            self.block_id = self._io.read_u8le()
            self.version = self._io.read_u8le()
            self.type_block = self._root.BlockType(self._io.read_u2le())
            self.flags = self._io.read_u2le()
            self.type_content = self._root.ContentType(self._io.read_u2le())
            self.padding = self._io.read_u2le()


    class CheckpointEntry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type_block = self._root.BlockType(self._io.read_u2le())
            self.flags = self._io.read_u2le()
            self.type_content = self._root.ContentType(self._io.read_u4le())
            self.block_size = self._io.read_u4le()
            self.unknown_52 = self._io.read_u4le()
            self.unknown_56 = self._io.read_u4le()
            self.unknown_60 = self._io.read_u4le()
            self.block_id = self._io.read_u8le()
            self.block = self._root.RefBlock(self._io, self, self._root)


    class Containersuperblock(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.ensure_fixed_contents(struct.pack('4b', 78, 88, 83, 66))
            self.block_size = self._io.read_u4le()
            self.num_blocks = self._io.read_u8le()
            self.padding = self._io.read_bytes(16)
            self.unknown_64 = self._io.read_u8le()
            self.guid = self._io.read_bytes(16)
            self.next_free_block_id = self._io.read_u8le()
            self.next_version = self._io.read_u8le()
            self.unknown_104 = self._io.read_bytes(32)
            self.previous_containersuperblock_block = self._io.read_u4le()
            self.unknown_140 = self._io.read_bytes(12)
            self.spaceman_id = self._io.read_u8le()
            self.block_map_block = self._root.RefBlock(self._io, self, self._root)
            self.unknown_168_id = self._io.read_u8le()
            self.padding2 = self._io.read_u4le()
            self.num_volumesuperblock_ids = self._io.read_u4le()
            self.volumesuperblock_ids = [None] * (self.num_volumesuperblock_ids)
            for i in range(self.num_volumesuperblock_ids):
                self.volumesuperblock_ids[i] = self._io.read_u8le()



    class NamedRecord(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.node_id = self._io.read_u8le()
            self.timestamp = self._io.read_u8le()
            self.type_item = self._root.ItemType(self._io.read_u2le())


    class AllocationinfofileEntry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.version = self._io.read_u8le()
            self.unknown_8 = self._io.read_u4le()
            self.unknown_12 = self._io.read_u4le()
            self.num_blocks = self._io.read_u4le()
            self.num_free_blocks = self._io.read_u4le()
            self.allocationfile_block = self._io.read_u8le()


    class ExtentRecord(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.size = self._io.read_u8le()
            self.block_num = self._root.RefBlock(self._io, self, self._root)
            self.unknown_16 = self._io.read_u8le()


    class Key(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.key_low = self._io.read_u4le()
            self.key_high = self._io.read_u4le()
            _on = self.type_entry
            if _on == self._root.EntryType.location:
                self.content = self._root.LocationKey(self._io, self, self._root)
            elif _on == self._root.EntryType.inode:
                self.content = self._root.InodeKey(self._io, self, self._root)
            elif _on == self._root.EntryType.extent:
                self.content = self._root.ExtentKey(self._io, self, self._root)
            elif _on == self._root.EntryType.extattr:
                self.content = self._root.NamedKey(self._io, self, self._root)
            elif _on == self._root.EntryType.hardlink:
                self.content = self._root.HardlinkKey(self._io, self, self._root)
            elif _on == self._root.EntryType.name:
                self.content = self._root.NamedKey(self._io, self, self._root)

        @property
        def key_value(self):
            if hasattr(self, '_m_key_value'):
                return self._m_key_value if hasattr(self, '_m_key_value') else None

            self._m_key_value = (self.key_low + ((self.key_high & 268435455) << 32))
            return self._m_key_value if hasattr(self, '_m_key_value') else None

        @property
        def type_entry(self):
            if hasattr(self, '_m_type_entry'):
                return self._m_type_entry if hasattr(self, '_m_type_entry') else None

            self._m_type_entry = self._root.EntryType((self.key_high >> 28))
            return self._m_type_entry if hasattr(self, '_m_type_entry') else None


    class HardlinkRecord(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.node_id = self._io.read_u8le()
            self.namelength = self._io.read_u2le()
            self.dirname = (self._io.read_bytes(self.namelength)).decode(u"UTF-8")


    class T6Record(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unknown_0 = self._io.read_u4le()


    class DynamicEntryHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ofs_key = self._io.read_s2le()
            if (self._parent._parent.type_flags & 4) == 0:
                self.len_key = self._io.read_u2le()

            self.ofs_data = self._io.read_s2le()
            if (self._parent._parent.type_flags & 4) == 0:
                self.len_data = self._io.read_u2le()



    class Block(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.header = self._root.BlockHeader(self._io, self, self._root)
            _on = self.header.type_block
            if _on == self._root.BlockType.node:
                self.body = self._root.Node(self._io, self, self._root)
            elif _on == self._root.BlockType.allocationinfofile:
                self.body = self._root.Allocationinfofile(self._io, self, self._root)
            elif _on == self._root.BlockType.spaceman:
                self.body = self._root.Spaceman(self._io, self, self._root)
            elif _on == self._root.BlockType.btree:
                self.body = self._root.Btree(self._io, self, self._root)
            elif _on == self._root.BlockType.rootnode:
                self.body = self._root.Node(self._io, self, self._root)
            elif _on == self._root.BlockType.volumesuperblock:
                self.body = self._root.Volumesuperblock(self._io, self, self._root)
            elif _on == self._root.BlockType.checkpoint:
                self.body = self._root.Checkpoint(self._io, self, self._root)
            elif _on == self._root.BlockType.containersuperblock:
                self.body = self._root.Containersuperblock(self._io, self, self._root)


    class PointerRecord(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pointer = self._io.read_u8le()


    class ExtattrRecord(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type_ea = self._root.EaType(self._io.read_u2le())
            self.len_data = self._io.read_u2le()
            _on = self.type_ea
            if _on == self._root.EaType.symlink:
                self.data = (KaitaiStream.bytes_terminate(self._io.read_bytes(self.len_data), 0, False)).decode(u"UTF-8")
            else:
                self.data = self._io.read_bytes(self.len_data)


    class RefBlock(KaitaiStruct):
        """Universal type to address a block: it both parses one u8-sized
        block address and provides a lazy instance to parse that block
        right away.
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.value = self._io.read_u8le()

        @property
        def target(self):
            if hasattr(self, '_m_target'):
                return self._m_target if hasattr(self, '_m_target') else None

            io = self._root._io
            _pos = io.pos()
            io.seek((self.value * self._root.block_size))
            self._raw__m_target = io.read_bytes(self._root.block_size)
            io = KaitaiStream(BytesIO(self._raw__m_target))
            self._m_target = self._root.Block(io, self, self._root)
            io.seek(_pos)
            return self._m_target if hasattr(self, '_m_target') else None


    class T12Record(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unknown_0 = self._io.read_u8le()


    class HardlinkKey(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.id2 = self._io.read_u8le()


    class Checkpoint(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unknown_0 = self._io.read_u4le()
            self.num_entries = self._io.read_u4le()
            self.entries = [None] * (self.num_entries)
            for i in range(self.num_entries):
                self.entries[i] = self._root.CheckpointEntry(self._io, self, self._root)



    class Btree(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unknown_0 = self._io.read_bytes(16)
            self.root = self._root.RefBlock(self._io, self, self._root)


    class Node(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type_flags = self._io.read_u2le()
            self.leaf_distance = self._io.read_u2le()
            self.num_entries = self._io.read_u4le()
            self.unknown_40 = self._io.read_u2le()
            self.ofs_keys = self._io.read_u2le()
            self.len_keys = self._io.read_u2le()
            self.ofs_data = self._io.read_u2le()
            self.meta_entry = self._root.FullEntryHeader(self._io, self, self._root)
            self.entries = [None] * (self.num_entries)
            for i in range(self.num_entries):
                self.entries[i] = self._root.NodeEntry(self._io, self, self._root)



    class ThreadRecord(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.parent_id = self._io.read_u8le()
            self.node_id = self._io.read_u8le()
            self.timestamps = [None] * (4)
            for i in range(4):
                self.timestamps[i] = self._io.read_u8le()

            self.flags = self._io.read_u4le()
            self.unknown_52 = self._io.read_u4le()
            self.unknown_56 = self._io.read_u8le()
            self.unknown_64 = self._io.read_u8le()
            self.owner_id = self._io.read_u4le()
            self.group_id = self._io.read_u4le()
            self.access = self._io.read_u4le()
            self.unknown_84 = self._io.read_u4le()
            self.unknown_88 = self._io.read_u4le()
            self.filler_flag = self._io.read_u2le()
            self.unknown_94 = self._io.read_u2le()
            self.unknown_96 = self._io.read_u2le()
            self.len_name = self._io.read_u2le()
            if self.filler_flag == 2:
                self.name_filler = self._io.read_u4le()

            self.name = (self._io.read_bytes_term(0, False, True, True)).decode(u"UTF-8")
            if (self._io.pos() % 1) != 0:
                self.padding1 = self._io.read_u1()

            if (self._io.pos() % 2) != 0:
                self.padding2 = self._io.read_u2le()

            self.logical_size = self._io.read_u8le()
            self.physical_size = self._io.read_u8le()
            self.unk1 = self._io.read_u8le()
            self.logical_size2 = self._io.read_u8le()
            self.unk2 = self._io.read_u8le()
            self.unknown_remainder = self._io.read_bytes_full()


    class InodeRecord(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.block_count = self._io.read_u4le()
            self.unknown_4 = self._io.read_u2le()
            self.block_size = self._io.read_u2le()
            self.inode = self._io.read_u8le()
            self.unknown_16 = self._io.read_u4le()


    class InodeKey(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.block_num = self._root.RefBlock(self._io, self, self._root)


    class NamedKey(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.len_name = self._io.read_u1()
            self.flag_1 = self._io.read_u1()
            if self.flag_1 != 0:
                self.unknown_2 = self._io.read_u2le()

            self.dirname = (KaitaiStream.bytes_terminate(self._io.read_bytes(self.len_name), 0, False)).decode(u"UTF-8")


    class Spaceman(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.block_size = self._io.read_u4le()
            self.unknown_36 = self._io.read_bytes(12)
            self.num_blocks = self._io.read_u8le()
            self.unknown_56 = self._io.read_bytes(8)
            self.num_entries = self._io.read_u4le()
            self.unknown_68 = self._io.read_u4le()
            self.num_free_blocks = self._io.read_u8le()
            self.ofs_entries = self._io.read_u4le()
            self.unknown_84 = self._io.read_bytes(92)
            self.prev_allocationinfofile_block = self._io.read_u8le()
            self.unknown_184 = self._io.read_bytes(200)

        @property
        def allocationinfofile_blocks(self):
            if hasattr(self, '_m_allocationinfofile_blocks'):
                return self._m_allocationinfofile_blocks if hasattr(self, '_m_allocationinfofile_blocks') else None

            _pos = self._io.pos()
            self._io.seek(self.ofs_entries)
            self._m_allocationinfofile_blocks = [None] * (self.num_entries)
            for i in range(self.num_entries):
                self._m_allocationinfofile_blocks[i] = self._io.read_u8le()

            self._io.seek(_pos)
            return self._m_allocationinfofile_blocks if hasattr(self, '_m_allocationinfofile_blocks') else None


    class HistoryKey(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.version = self._io.read_u8le()
            self.block_num = self._root.RefBlock(self._io, self, self._root)


    @property
    def block_size(self):
        if hasattr(self, '_m_block_size'):
            return self._m_block_size if hasattr(self, '_m_block_size') else None

        self._m_block_size = self._root.block0.body.block_size
        return self._m_block_size if hasattr(self, '_m_block_size') else None


