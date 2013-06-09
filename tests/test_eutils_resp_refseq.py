import os,unittest

import eutils.resp.refseq

data_dir = os.path.realpath(os.path.realpath( os.path.join(__file__,'../data')))

class Test_eutils_resp_refseq_RefSeq(unittest.TestCase):
    def test_NEFL(self):
        xml = open(os.path.join(data_dir,'efetch.fcgi?db=nuccore&id=148536845&retmode=xml.xml')).read()
        rs = eutils.resp.refseq.RefSeq(xml)
        self.assertEqual(rs.acv, 'NM_023035.2')
        self.assertEqual(rs.cds_start_end, (237, 7775))
        self.assertEqual(rs.cds_start_end_i, (236, 7775))
        self.assertEqual(rs.chr,'19')
        self.assertEqual(rs.exon_names, ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10a',
                                         '11', '12', '13', '14', '15', '16', '17b', '18', '19',
                                         '20', '21', '22', '23', '24', '25', '26', '27', '28', '29',
                                         '30', '31', '32', '33', '34', '35', '36', '37', '39', '40',
                                         '41', '42', '43', '44', '45', '46', '47', '48', '49a'])
        self.assertEqual(rs.exons,  [(0, 529), (529, 635), (635, 775), (775, 867), (867, 1020),
                                     (1020, 1214), (1214, 1318), (1318, 1434), (1434, 1491), (1491, 1584),
                                     (1584, 1794), (1794, 1907), (1907, 2020), (2020, 2152), (2152, 2225),
                                     (2225, 2343), (2343, 2420), (2420, 2527), (2527, 3337), (3337, 3801),
                                     (3801, 3940), (3940, 4070), (4070, 4130), (4130, 4237), (4237, 4337),
                                     (4337, 4498), (4498, 4636), (4636, 4838), (4838, 5003), (5003, 5114),
                                     (5114, 5198), (5198, 5204), (5204, 5321), (5321, 5387), (5387, 5503),
                                     (5503, 5654), (5654, 5782), (5782, 5879), (5879, 5985), (5985, 6093),
                                     (6093, 6194), (6194, 6304), (6304, 6443), (6443, 6557), (6557, 6593),
                                     (6593, 6780), (6780, 7034), (7034, 8646)] )
        self.assertEqual(rs.gene, ['CACNA1A'])
        self.assertEqual(rs.hgnc, ['CACNA1A'])
        self.assertTrue(rs.seq.startswith('gatgtcccga'))
        self.assertTrue(rs.seq.endswith('ttgaatcaaa'))
        self.assertTrue(len(rs.seq) == 8646)

                         
if __name__ == '__main__':
    unittest.main()
