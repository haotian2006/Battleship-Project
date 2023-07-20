'''
Created on Mar 5, 2021

5 basic tests to test the API's of isSet, playRound and displayInRows

Meant to be a check to see if submissions meet a minimum capabiility

@author: makwong
'''
import unittest
import re
from io import StringIO
from itertools import permutations
from unittest.mock import patch
from random import shuffle

from battleshipplayer import BattleshipPlayer
from display import Display
from oceanboard import OceanBoard
from targetboard import TargetBoard
from ship import Ship
from game import playBattleship

class Test(unittest.TestCase):

    def testSubmission(self):
        self.assertTrue(True, "submission was successful")

    def testTargetBoardBasic(self):
        t = TargetBoard(10,10)
        self.assertFalse(t.isHit(1,3))

        t.markHit(1,3)
        self.assertTrue(t.isHit(1,3))

        self.assertTrue(t.isEmpty(4,5))
        t.markMiss(4,5)
        self.assertFalse(t.isHit(4,5))
        self.assertFalse(t.isEmpty(4,5))

    def testShipBasic(self):
        ship = Ship("Battleship", 4)
        ship.setLocation(3, 5)
        ship.setHorizontal(True)

        ship.markHitAt(3, 6)
        ship.markHitAt(3, 7)
        self.assertTrue(ship.isHitAt(3, 7), "isHit(3, 7) should be True")
        self.assertFalse(ship.isHitAt(3, 8), "isHit(3, 8) should be False")

        self.assertFalse(ship.isSunk(), "isSunk() should be false after only 2 hits")

        ship.markHitAt(3, 5)
        ship.markHitAt(3, 8)
        self.assertTrue(ship.isSunk(), "isSunk() should be true after 4 hits")

    def testOceanBoardBasic(self):
        ocean = OceanBoard(10, 10)
        carrier = Ship("Carrier", 5)
        placed = ocean.placeShip(carrier, 1, 2, 'v')
        self.assertTrue(placed, "placeShip() of Carrier @ (1, 2) vertically")

        r, c = carrier.getLocation()
        self.assertEqual((r, c), (1, 2), "carrier.getLocation() should be (1, 2)")
        self.assertFalse(carrier.isHorizontal(), "carrier should be vertical")
        
        battleship = Ship("Battleship", 4)
        placed = ocean.placeShip(battleship, 2, 1, 'h')
        self.assertFalse(placed, "placeShip() of battleship @ (2, 1) horizontal")

    def testBattleShipPlayerBasic(self):
        player = BattleshipPlayer("Mark", 10, 10)
        placed = player.placeShip(Ship("Carrier", 5), 'b3', 'v')
        self.assertTrue(placed, "Carrier placed @ b3 vertical OK")

        self.assertEqual(None, player.shipAt(0,0), "No ship at (0, 0)")
        self.assertNotEqual(None, player.shipAt(1,2), "Ship at (1, 2)")

        self.assertFalse(player.allShipsSunk(), "allShipsSunk() - not yet...")

        (hit, sunk, name) = player.shotAt(0,0)
        self.assertFalse(hit, "shotAt(0,0)")
        self.assertEqual((True, False, "Carrier"), player.shotAt(1,2), "shotAt(1,2)")
        self.assertEqual((True, False, "Carrier"), player.shotAt(2,2), "shotAt(2,2)")
        self.assertEqual((True, False, "Carrier"), player.shotAt(3,2), "shotAt(3,2)")
        self.assertEqual((True, False, "Carrier"), player.shotAt(4,2), "shotAt(4,2)")
        self.assertEqual((True, True, "Carrier"), player.shotAt(5,2), "shotAt(5,2)")

        self.assertTrue(player.allShipsSunk(), "allShipsSunk() - the carrier is sunk")

        player.updateScore(10)
        self.assertEqual(10, player.getScore(), "updateScore(10)")

        self.assertFalse(player.target.isHit(5, 7), "isHit(5, 7) False")
        player.markTargetHit(5, 7)
        self.assertTrue(player.target.isHit(5, 7), "isHit(5, 7) True")
        self.assertFalse(player.target.isEmpty(5, 7), "isEmpty(5, 7) False")
        
        self.assertTrue(player.target.isEmpty(6, 3), "isEmpty(6, 3) True")
        player.markTargetMiss(6,3)
        self.assertFalse(player.target.isHit(6, 3), "isHit(6, 3) False")
        self.assertFalse(player.target.isEmpty(6, 3), "isEmpty(6, 3) False")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
