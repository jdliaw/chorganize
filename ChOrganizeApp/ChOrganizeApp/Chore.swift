//
//  Chore.swift
//  ChOrganizeApp
//
//  Created by Hana on 11/10/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit
import os.log

class Chore/*: NSObject, NSCoding*/ { // NSCoding to persist data across the app
    init?(name: String, date: String) {
        if name.isEmpty || date.isEmpty {
            return nil
        }
        self.name = name
        self.date = date
    }
    
//    // NSCoding init, to decode the fields needed
//    required convenience init?(coder aDecoder: NSCoder) {
//        guard let name = aDecoder.decodeObject(forKey: PropertyKey.name) as? String else {
//            os_log("Unable to decode a name for the Chore object", log: OSLog.default, type: .debug)
//            return nil
//        }
//        let date = aDecoder.decodeObject(forKey: PropertyKey.date) as? String
//        
//        self.init(name: name, date: date!)
//    }
    
    var name: String
    var date: String
    
//    static let DocumentsDirectory = FileManager().urls(for: .documentDirectory, in: .userDomainMask).first!
//    static let ArchiveURL = DocumentsDirectory.appendingPathComponent("chores")
//    
//    // Keys used to recognize fields in Chore as strings
//    struct PropertyKey {
//        static let name = "name"
//        static let date = "date"
//    }
//    
//    // Encoding to persist data
//    func encode(with aCoder: NSCoder) {
//        aCoder.encode(name, forKey: PropertyKey.name)
//        aCoder.encode(date, forKey: PropertyKey.date)
//    }
}
