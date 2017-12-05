//
//  ToDo.swift
//  ChOrganizeApp
//
//  Created by Hana on 11/10/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class ToDoTableViewCell: UITableViewCell {

    //MARK: Properties
    @IBOutlet weak var cell: UIView!
    @IBOutlet weak var nameLabel: UILabel!
    @IBOutlet weak var checkBoxButton: UIButton!
    @IBOutlet weak var dateLabel: UILabel!
    
//    let checkBox = UIImage(named: "CheckBox")
//    let uncheckBox = UIImage(named: "UnCheckBox")
//    var isboxclicked: Bool!
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }
    
//    @IBAction func clickBox(_ sender: AnyObject) {
//        if isboxclicked == true {
//            isboxclicked = false
//        } else {
//            isboxclicked = true
//        }
//        
//        if isboxclicked == true {
//            checkBoxButton.setImage(checkBox, for: UIControlState.normal)
//        } else {
//            checkBoxButton.setImage(uncheckBox, for: UIControlState.normal)
//        }
//    }
}
